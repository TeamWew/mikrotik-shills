import os, ipaddress
import urllib.request, urllib.error

# TeamWew is Life
# TeamWew is Love
# TeamWew is Eternal
# Aciid 2020
# Greetings to Antihawk, Narchie, Deffi, TIEDL-OS, Berner, Panaman Nalle, Hirmut jne
#
# https://doc.emergingthreats.net/
# https://doc.emergingthreats.net/bin/view/Main/EmergingFAQ
# This list is the brass and roots that a ((( company ))) uses commercially in shithole SF Cali.
#
# How to use
# Run script,
# Transfer to created "mikorotiklist.txt" to "files" and use /import mikrotiklist.txt
# OR copy paste contents to terminal
#
# After successful import add a filter rule to start using.
# /ip firewall filter
# add action=drop chain=input,forward src-address-list=emerging


def readPrevRev():  # read earlier fwrev to variable
  with open("./FWrev", "r") as f:
    data = f.read()
  return data

def transformBlockList():
  validatedIps = []
  with open("./emerging-Block-IPs.txt", "r") as f:
    content = f.readlines()
    content = [x.strip() for x in content]  # remove empty lines
    for x in content:
      try:
        ip = ipaddress.ip_network(x)
        validatedIps.append(ip.compressed)
      except ValueError:
        pass
    f.close()
  with open("./mikrotiklist.txt", "w") as f:
    # Remove earlier address-list entries for emerging
    f.write('/ip firewall address-list remove [/ip firewall address-list find list="emerging"]\n')
    # Create new address-list
    f.write('/ip firewall address-list\n')
    for x in validatedIps:
      f.write('add address={} list="emerging"\n'.format(x))
    f.close()

# TODO: emergingthreats cdn is slow sometimes
def downloadRev():
  url = 'https://rules.emergingthreats.net/fwrules/FWrev'
  try:
    data = urllib.request.urlretrieve(url, "./FWrev")
    return data
  except urllib.request.HTTPError as e:
    print(e)

# TODO: emergingthreats cdn is slow sometimes
def downloadLatest():
  url = 'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt'
  try:
    urllib.request.urlretrieve(url, "./emerging-Block-IPs.txt")
  except urllib.request.HTTPError as e:
    print(e)

if __name__ == "__main__":

  # FIXME: methodically assert variable scope
  earlierRev = 0
  latestRev = 0

  # Determine first run
  try:
    earlierRev = readPrevRev()  # Read earlier rev information to var for later
    print("[*] Reminisce of previous version, removing cached rev")
    os.remove("./FWrev")
  except IOError:
    print("[*] No reminisce of previous revision, downloading rev information")
    downloadRev()
  finally:
    print("[*] Download latest rev information for comparison")
    downloadRev()

  # Compare
  latestRev = readPrevRev()
  if earlierRev != latestRev:
    downloadLatest()
    print("[*] Transforming blocklist")
    transformBlockList()
    print("[*] All done")
  else:
    print("[*] List up to date exit")






