#!/opt/homebrew/bin/python3.9
# coding=utf-8
from .entity import Entity
from .segment import Segment
from .transportzone import TransportZone
from .nsxcluster import NSXCluster, NSXManager, NSXClusterSchema
from ..lib import system, nsxconnection
from src.constants import constants
from marshmallow import Schema, fields


class NSX_Infra:
    def __init__(self, name, session, vip):
        Entity.__init__(self)
        if not hasattr(type(self), '_infra'):
            self._create_infra(name, session, vip)


    @classmethod
    def _create_infra(self, name, session, vip):
        print("==> Creating Infra for: " + vip  + " - " + system.style.GREEN + "Successful" + system.style.NORMAL)
        self.name = name
        self.session = session
        self.tz = []
        self.vip = vip
        self.version = ""
        self.siteid = ""
        self.domainid = ""
        self.enforcementpointid = ""
        self.cluster = None
        self.nodes = []
        self.segments = []
        self.swagger = None

    def discovery(self):
        print("==> Discovering")
        self.add_tz()
        self.add_segments()
        self.add_cluster()

        
    ################################################################################################
    # Transport Zone functions
    def add_tz(self):
        print("==> Looking up for Transport Zones")

        tz_result = self.session.get(constants.constants['URL']['TZ'])
        if tz_result.status_code == 200 and 'results' in tz_result.json():
            for tzone in tz_result.json()['results']:
                # check if segment is not already on the list
                tz_found = system.search_obj_in_list(self.tz, 'id', tzone['id'])
                if tz_found is None:
                    self.tz.append(TransportZone(tzone['display_name'], tzone['tz_type'],tzone['id'], tzone['is_default'], tzone['path']))

        print("== ==> Nb Transport Zone " + system.style.GREEN + str(len(self.tz))  + system.style.NORMAL)

    ################################################################################################
    # Clsuter Status
    def add_cluster(self):
        print("==> Looking up for NSX Cluster")
        # Get NSX Version
        node_result = self.session.get(constants.constants['URL']['NSX_VERSION'])
        node_json = node_result.json()
        if node_result.status_code == 200:
            self.version = node_json["product_version"]
        
        # Get NSX Cluster
        cluster_result = self.session.get(constants.constants['URL']['NSX_CLUSTER'])
        result_json = cluster_result.json()
        if cluster_result.status_code == 200:
            self.cluster = NSXCluster(result_json['cluster_id'], result_json['mgmt_cluster_status']['status'], result_json['detailed_cluster_status']['overall_status'])
            
            # Members
            for member in result_json['detailed_cluster_status']['groups'][0]['members']:
                self.cluster.members.append(NSXManager(member['member_uuid'], member['member_ip'], member['member_fqdn'], member['member_status']))
            # online and offline managers
            for member in result_json['mgmt_cluster_status']['online_nodes']:
                mb = system.search_obj_in_list(self.cluster.members, 'id', member['uuid'])
                if member['uuid'] == mb.id and mb not in self.cluster.online_node:
                    self.cluster.online_node.append(mb)
            for member in result_json['mgmt_cluster_status']['offline_nodes']:
                mb = system.search_obj_in_list(self.cluster.members, 'id', member['uuid'])
                if member['uuid'] == mb.id and mb not in self.cluster.online_node:
                    self.cluster.offline_node.append(mb)


    ################################################################################################
    # Segments functions
    def add_segments(self):
        print("==> Looking up for segments")
        seg_result = self.session.get(constants.constants['URL']['SEGMENTS'])

        if seg_result.status_code == 200 and 'results' in seg_result.json():
            for segment in seg_result.json()['results']:
                sg = Segment(segment['display_name'], segment['id'], segment['unique_id'])
                sg.type = segment['type']
                sg.connectivity = segment['advanced_config']['connectivity']
                sg.admin_state = segment['admin_state']
                sg.type = segment['type']
                if 'vni' in segment: sg.vni = segment['vni']
                if 'vlan' in segment: sg.vlan = segment['vlan']
                sg.replication_mode = segment.get('replication_mode')
                tz = system.search_obj_in_list(self.tz, 'path', segment['transport_zone_path'])
                sg.transportzone_obj = tz
                sg.segment_type = tz.type.split('_')[0]
                # check if segment is not already on the list
                sg_found = system.search_obj_in_list(self.segments, 'id', segment['id'])
                if sg_found is None:
                    self.segments.append(sg)

        print("== ==> Nb Segments " + system.style.GREEN + str(len(self.segments))  + system.style.NORMAL)

class InfraSchema(Schema):
    name = fields.Str()
    session = fields.Nested(nsxconnection.NSXConnectionSchema(only=("nsx","login", "method")))
    vip = fields.Str()
    version = fields.Str()
    siteid = fields.Str()
    domainid = fields.Str()
    enforcementpointid = fields.Str()
    cluster = fields.Nested(NSXClusterSchema)
    tz = fields.List(fields.Nested(NSXClusterSchema))
    segments = fields.List(fields.Nested(NSXClusterSchema))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()