#!/opt/homebrew/bin/python3.9
# coding=utf-8

from src.lib import nsxconnection, system
from src.entities import segment, infra, transportzone
from flask import Flask, jsonify, request


yaml_cfg = './src/config.yml'
print("==> Read YAML config file: " + system.style.ORANGE + yaml_cfg + system.style.NORMAL)
dict_cfg = system.Read_Yaml(yaml_cfg)

nsx_session = nsxconnection.NSX_Session(dict_cfg['NSX_IP'], dict_cfg['NSX_LOGIN'], dict_cfg['NSX_PASSWORD'], 'session')
nsx_infra = infra.NSX_Infra("Lab",nsx_session, dict_cfg['NSX_IP'])

app = Flask('PowerOps')

@app.route('/')
def hello_world():
    return 'Welcome to PowerOps NG'

@app.route('/segments')
def get_segments():
    # transforming into JSON-serializable objects
    segments = nsx_infra.segments
    schema = segment.SegmentSchema(many=True)
    segs = schema.dump(segments)
    # serializing as JSON
    return jsonify(segs)

@app.route('/transportzones')
def get_tz():
    # transforming into JSON-serializable objects
    zones = nsx_infra.tz
    schema = transportzone.TZSchema(many=True)
    tz = schema.dump(zones)
    # serializing as JSON
    return jsonify(tz)

# nsx_session.destroy_session()
