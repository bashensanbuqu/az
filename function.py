# coding:utf8
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials
import json

from azure.mgmt.subscription import SubscriptionClient
import time, base64


def create_credential_object(tenant_id, client_id, client_secret):
    print("Create Credential Object")
    tenant_id = tenant_id
    client_id = client_id
    client_secret = client_secret
    print(tenant_id," ",client_id," ",client_secret)
    credential = ServicePrincipalCredentials(tenant=tenant_id, client_id=client_id, secret=client_secret)
    return credential


def create_resource_group(subscription_id, credential, tag, location):
    print("Create eEsource Group")
    credential = credential
    resource_client = ResourceManagementClient(credential, subscription_id)
    RESOURCE_GROUP_NAME = tag
    LOCATION = location
    rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME,
                                                                 {
                                                                     "location": LOCATION
                                                                 }
                                                                 )


def create_or_update_vm(subscription_id, credential, tag, location, username, password, size, os, rootpwd, storgesize):
    global publisher, offer, sku
    compute_client = ComputeManagementClient(credential, subscription_id)
    RESOURCE_GROUP_NAME = tag
    VNET_NAME = ("vnet-" + tag)
    SUBNET_NAME = ("subnet-" + tag)
    IP_NAME = ("ip-" + tag)
    IP_CONFIG_NAME = ("ipconfig-" + tag)
    NIC_NAME = ("nicname-" + tag)
    LOCATION = location
    VM_NAME = tag
    USERNAME = username
    PASSWORD = password
    ROOT_PWD = rootpwd
    SIZE = size
    STORGESIZE = int(storgesize)
    if os == "debian11":
        publisher = "Debian"
        offer = "debian-11"
        sku = "11-gen2"
        version = "latest"
    elif os == "ubuntu20":
        publisher = "Canonical"
        offer = "0001-com-ubuntu-server-focal"
        sku = "20_04-lts-gen2"
        version = "latest"
    elif os == "ubuntu18":
        publisher = "Canonical"
        offer = "UbuntuServer"
        sku = "18.04-LTS"
        version = "latest"
    elif os == "ubuntu16":
        publisher = "Canonical"
        offer = "UbuntuServer"
        sku = "16.04.0-LTS"
        version = "latest"
    elif os == "centos":
        publisher = "OpenLogic"
        offer = "CentOS"
        sku = "7.5"
        version = "latest"
        
    elif os == "centos79":
        publisher = "OpenLogic"
        offer = "CentOS"
        sku = "7.9"
        version = "latest"
        
    elif os == "debian10":
        publisher = "Debian"
        offer = "debian-10"
        sku = "10"
        version = "latest"
    elif os == "windows2019":
        publisher = "MicrosoftWindowsServer"
        offer = "WindowsServer"
        sku = "2019-Datacenter-smalldisk"
        version = "latest"
    elif os == "windows2016":
        publisher = "MicrosoftWindowsServer"
        offer = "WindowsServer"
        sku = "2016-Datacenter-smalldisk"
        version = "latest"
    elif os == "windows2012":
        publisher = "MicrosoftWindowsServer"
        offer = "WindowsServer"
        sku = "2012-Datacenter-smalldisk"
        version = "latest"
    elif os == "windows-server-2012-r2-datacenter-smalldisk-g2":
        publisher = "MicrosoftWindowsServer"
        offer = "WindowsServer"
        sku = "2012-r2-datacenter-smalldisk-g2"
        version = "latest"
    else:
        publisher = "Canonical"
        offer = "UbuntuServer"
        sku = "18.04-LTS"
        version = "latest"

    network_client = NetworkManagementClient(credential, subscription_id)
    print("Create VNET")
    poller = network_client.virtual_networks.create_or_update(RESOURCE_GROUP_NAME,
                                                              VNET_NAME,
                                                              {
                                                                  "location": LOCATION,
                                                                  "address_space": {
                                                                      "address_prefixes": ["10.0.0.0/16"]
                                                                  }
                                                              }
                                                              )
    vnet_result = poller.result()
    print("Create Subnets")
    poller = network_client.subnets.create_or_update(RESOURCE_GROUP_NAME,
                                                     VNET_NAME, SUBNET_NAME,
                                                     {"address_prefix": "10.0.0.0/24"}
                                                     )
    subnet_result = poller.result()
    print("Create IP")
    poller = network_client.public_ip_addresses.create_or_update(RESOURCE_GROUP_NAME,
                                                                 IP_NAME,
                                                                 {
                                                                     "location": LOCATION,
                                                                     "sku": {"name": "Basic"},
                                                                     "public_ip_allocation_method": "Dynamic",
                                                                     "public_ip_address_version": "IPV4"
                                                                 }
                                                                 )
    ip_address_result = poller.result()
    print("Create Network Interfaces")
    poller = network_client.network_interfaces.create_or_update(RESOURCE_GROUP_NAME,
                                                                NIC_NAME,
                                                                {
                                                                    "location": LOCATION,
                                                                    "ip_configurations": [{
                                                                        "name": IP_CONFIG_NAME,
                                                                        "subnet": {"id": subnet_result.id},
                                                                        "public_ip_address": {
                                                                            "id": ip_address_result.id}
                                                                    }],
                                                                }
                                                                )
    nic_result = poller.result()
    s = "IyEvYmluL2Jhc2gKZWNobyByb290OnBweHdvMTIzIHxzdWRvIGNocGFzc3dkIHJvb3QKc3VkbyBzZWQgLWkgJ3MvXi4qUGVybWl0Um9vdExvZ2luLiovUGVybWl0Um9vdExvZ2luIHllcy9nJyAvZXRjL3NzaC9zc2hkX2NvbmZpZzsKc3VkbyBzZWQgLWkgJ3MvXi4qUGFzc3dvcmRBdXRoZW50aWNhdGlvbi4qL1Bhc3N3b3JkQXV0aGVudGljYXRpb24geWVzL2cnIC9ldGMvc3NoL3NzaGRfY29uZmlnOwpzdWRvIHNlcnZpY2Ugc3NoZCByZXN0YXJ0"
    if (ROOT_PWD != ""):
        d = base64.b64decode(s).decode('latin-1')
        d = d.replace("ppxwo123", ROOT_PWD)
        CUSTOM_DATA = base64.b64encode(d.encode("utf-8")).decode('latin-1')
    else:
        CUSTOM_DATA = s
    poller = compute_client.virtual_machines.create_or_update(RESOURCE_GROUP_NAME, VM_NAME,
                                                              {
                                                                  "location": LOCATION,
                                                                  "storage_profile": {
                                                                      "osDisk": {
                                                                          "createOption": "fromImage",
                                                                          "diskSizeGB": STORGESIZE
                                                                      },
                                                                      "image_reference": {
                                                                          "offer": offer,
                                                                          "publisher": publisher,
                                                                          "sku": sku,
                                                                          "version": version
                                                                      }
                                                                  },
                                                                  "hardware_profile": {
                                                                      "vm_size": SIZE
                                                                  },
                                                                  "os_profile": {
                                                                      "computer_name": VM_NAME,
                                                                      "admin_username": USERNAME,
                                                                      "admin_password": PASSWORD,
                                                                      "custom_data": CUSTOM_DATA
                                                                  },
                                                                  "network_profile": {
                                                                      "network_interfaces": [{
                                                                          "id": nic_result.id,
                                                                      }],
                                                                  }
                                                              }
                                                              )
    vm_result = poller.result()
    print(vm_result)


def start_vm(subscription_id, credential, tag):
    compute_client = ComputeManagementClient(credential, subscription_id)
    GROUP_NAME = tag
    VM_NAME = tag
    async_vm_start = compute_client.virtual_machines.start(
        GROUP_NAME, VM_NAME)
    async_vm_start.wait()


def stop_vm(subscription_id, credential, tag):
    compute_client = ComputeManagementClient(credential, subscription_id)
    GROUP_NAME = tag
    VM_NAME = tag
    async_vm_deallocate = compute_client.virtual_machines.deallocate(
        GROUP_NAME, VM_NAME)
    async_vm_deallocate.wait()


def delete_vm(subscription_id, credential, tag):
    resource_client = ResourceManagementClient(credential, subscription_id)
    GROUP_NAME = tag
    resource_client.resource_groups.delete(GROUP_NAME)


def change_ip(subscription_id, credential, tag):
    compute_client = ComputeManagementClient(credential, subscription_id)
    GROUP_NAME = tag
    VM_NAME = tag
    async_vm_deallocate = compute_client.virtual_machines.deallocate(
        GROUP_NAME, VM_NAME)
    async_vm_deallocate.wait()
    time.sleep(10)
    async_vm_start = compute_client.virtual_machines.start(
        GROUP_NAME, VM_NAME)
    async_vm_start.wait()


def list(subscription_id, credential):
    network_client = NetworkManagementClient(credential, subscription_id)
    info = network_client.public_ip_addresses.list_all()
    compute_client = ComputeManagementClient(credential, subscription_id)
    info2 = compute_client.virtual_machines.list_all()
    iplist = []
    ipnames = []

    for info in info:
        info = str(info)
        info = info.replace('"', '').replace('/', '').replace('None', '"None"').replace("'", '"').replace("<",
                                                                                                          '"').replace(
            ">", '"')
        info = json.loads(info)
        ipname = info["name"]
        ipname = ipname.replace('ip-', '')
        ipadd = info["ip_address"]
        iplist.append(ipadd)
        ipnames.append(ipname)

    for info2 in info2:
        info2 = str(info2)
        info2 = str(info2).replace("'", "").replace('"', "")
        info2 = info2.split(", ")[2].split(" ")[1]
        if info2 not in ipnames:
            ipnames.append(info2)
            iplist.append("None")
    dict = {"ip": iplist, "tag": ipnames}

    subscription_client = SubscriptionClient(credential)
    names = []
    idstatus = []
    for subscription in subscription_client.subscriptions.list():
        names.append(subscription.display_name)
        idstatus.append(subscription.subscription_id + " " + str(subscription.state).replace('SubscriptionState.', ''))
    dic = {"name": names, "id_status": idstatus}


    return dict,dic


