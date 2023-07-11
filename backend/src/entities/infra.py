#!/opt/homebrew/bin/python3.9
# coding=utf-8

from .segment import Segment
from .transportzone import TransportZone
from ..lib import system
from src.constants import constants


class NSX_Infra:
    def __init__(self, name, session, vip):

        if not hasattr(type(self), '_infra'):
            self._create_infra(name, session, vip)


    @classmethod
    def _create_infra(self, name, session, vip):
        print("==> Creating Infra for: " + vip  + " - " + system.style.GREEN + "Successful" + system.style.NORMAL)

        self.name = name
        self.session = session
        self.tz = self.add_tz_list(self, session)
        self.name = name
        self.vip = vip
        self.version = ""
        self.siteid = ""
        self.domainid = ""
        self.enforcementpointid = ""
        self.cluster = None
        self.nodes = []
        self.segments = self.add_segments_list(self, session)
        self.swagger = None


    def show(self):
        print('Infra:')
        print(' - name: ' + self.name)
        print(' - site: ' + self.siteid)
        print(' - enforcement: ' + self.enforcementpointid)
        print(' - domain: ' + self.domainid)
        list_tz = []
        for tz in self.tz:
            list_tz.append(tz.name)
        print(' - tz: ' + ', '.join(list_tz))
        
    ################################################################################################
    # Transport Zone functions
    def add_tz_list(self, session):
        print("==> Looking up for Transport Zones")

        tz_result = session.get(constants.constants['URL']['TZ'])
        List_tz = []
        if tz_result.status_code == 200 and 'results' in tz_result.json():
            for tzone in tz_result.json()['results']:
                List_tz.append(TransportZone(tzone['display_name'], tzone['tz_type'],tzone['id'], tzone['is_default'], tzone['path']))

        print("== ==> Found " + system.style.GREEN + str(len(List_tz))  + system.style.NORMAL + " Transport Zones")
        return List_tz

    ################################################################################################
    # Segments functions

    def add_segments_list(self, session):
        print("==> Looking up for segments")
        seg_result = session.get(constants.constants['URL']['SEGMENTS'])
        List_segment = []

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
                sg.transportzone = tz.name
                sg.segment_type = tz.type.split('_')[0]
                List_segment.append(sg)

        print("== ==> Found " + system.style.GREEN + str(len(List_segment))  + system.style.NORMAL + " Segments")
        return List_segment