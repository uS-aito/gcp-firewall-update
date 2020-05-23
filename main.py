import requests
import subprocess

IPLIST_URL = "https://ipv4.fetus.jp/jp.txt"
FIREWALL_RULE_CREATE_COMMAND = "gcloud compute firewall-rules create {name} --allow={target_protocol} --source-ranges={range} --target-tags={target_tag}"
FIREWALL_NAME_PREFIX = "k8s-fw-"
TARGET_PROTOCOL = "TCP:8888"
TARGET_TAG = "gke-qlc-cluster-54ac5eeb-node"
dryrun = False

# https://ipv4.fetus.jp/jp.txtからIPのリストを取得
ip_list = requests.get(IPLIST_URL).text
# IPのリストをパースしてリストに変換
ip_list = ip_list.split("\n")
ip_list = [ip for ip in ip_list if len(ip) != 0 and ip[0] != "#"]
for i in range(int(len(ip_list)/256)+1):
    ip_range = ",".join(ip_list[i*256:(i+1)*256])
# gcloudコマンドを実行
    cmd = FIREWALL_RULE_CREATE_COMMAND.format(name=FIREWALL_NAME_PREFIX+str(i), target_protocol=TARGET_PROTOCOL, range=ip_range, target_tag=TARGET_TAG)
    if dryrun:
        print(cmd)
    else:
        result = subprocess.run(cmd.split(" "))
        if result.stdout != None:
            print(result.stdout.decode("utf-8"))
        if result.stderr != None:
            print(result.stderr.decode("utf-8"))