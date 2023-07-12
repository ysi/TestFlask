#!/opt/homebrew/bin/python3.9
# coding=utf-8

from src.lib import nsxconnection, system
from src.entities import segment, infra, transportzone, nsxcluster
from flask import Flask, jsonify, render_template_string
import datetime


yaml_cfg = './src/config.yml'
print("==> Read YAML config file: " + system.style.ORANGE + yaml_cfg + system.style.NORMAL)
dict_cfg = system.Read_Yaml(yaml_cfg)

nsx_session = nsxconnection.NSX_Session(dict_cfg['NSX_IP'], dict_cfg['NSX_LOGIN'], dict_cfg['NSX_PASSWORD'], 'session')
nsx_infra = infra.NSX_Infra("Lab",nsx_session, dict_cfg['NSX_IP'])
nsx_infra.discovery()
app = Flask('PowerOps')

@app.route('/')
def hello_world():
    return render_template_string("""<!DOCTYPE html>
<html>

<head>
<meta charset="utf-8" />
<title>PowerOps NG</title>
</head>

<body>

NSX Cluster: <span id="time"><span>

<script type="text/javascript">
var time_span = document.getElementById("time");

function updater() {
  fetch('/update_cluster_status')
  .then(response => response.text())
  .then(text => (time_span.innerHTML = text));  // update page with new data
}

setInterval(updater, 5000);  // run `updater()` every 5000ms (5s)
</script>

</body>

</html>""")

@app.route('/update_cluster_status')
def update_cluster_status():
    """send current content"""
    # nsx_infra.cluster.update_status()
    # return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = nsx_infra.update_cluster_status() + " - " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return status

@app.route('/segments', methods=['GET'])
def get_segments():
    # transforming into JSON-serializable objects
    segments = nsx_infra.segments
    schema = segment.SegmentSchema(many=True)
    response = { 'result': schema.dump(segments)}
    # serializing as JSON
    return jsonify(response)

@app.route('/transportzones')
def get_tz():
    # transforming into JSON-serializable objects
    zones = nsx_infra.tz
    schema = transportzone.TZSchema(many=True)
    response = { 'result': schema.dump(zones)}
    # serializing as JSON
    return jsonify(response)

@app.route('/cluster')
def get_cluster():
    # transforming into JSON-serializable objects
    cl = nsx_infra.cluster
    schema = nsxcluster.NSXClusterSchema()
    response = { 'result': schema.dump(cl)}
    # serializing as JSON
    return jsonify(response)

@app.route('/infra')
def get_infra():
    # transforming into JSON-serializable objects
    schema = infra.InfraSchema()
    response = { 'result': schema.dump(nsx_infra)}
    # serializing as JSON
    return jsonify(response)

# nsx_session.destroy_session()
