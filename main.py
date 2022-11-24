'''
IMPORTANT : CE SCRIPT EST A EXECUTER UNIQUEMENT SUR UNE MACHINE LOCAL, LE SSH DOIT ÊTRE ACTIF SUR LE(S) SWITCH(S)
FONCTIONNE UNIQUEMENT AVEC LA VERSION AOS 5.0
TESTÉ SUR COMMUTATEUR ALCATEL LUCENT OMNI SWITCH 2360
POUR FONCTIONNER MERCI D'UTILISER PYTHON 3, AVEC LES MODULES MINICONDA (https://docs.conda.io/en/latest/miniconda.html), NETMIKO (pip install NETMIKO), PARAMIKO (conda install PARAMIKO)
EXECUTABLE DEPUIS WINDOWS, LINUX ET MACOS.
'''
import getpass
import time

import netmiko
from netmiko import ConnectHandler
from netmiko.alcatel.alcatel_aos_ssh import AlcatelAosSSH

__all__ = ["AlcatelAosSSH"]

'''
Système de connexion via SSH directement sur le switch
'''
print("Bienvenue sur le programme de provisionning de téléphones Alcatel Lucent sur Commutateur AOS 5.0")
print("Ce script à été réalisé par Ambroise Leroy (https://github.com/Ambroise105)")
print("Licence CC BY-SA 4.0 : https://he-arc.github.io/livre-python/licence.html")
print(" ")
time.sleep(1)

# On prend les informations SSH du switch #
host = input("Entrez l'adresse IP du switch Master au format (x.x.x.x): ") # Host de connexion
user = input("Entrez le nom d'utilisateur SSH (habituellement admin): ") # User de connexion
print("Entrez le mot de passe du switch (Ne s'affiche pas dans le prompt): ") # Mot de passe de connexion
password = getpass.getpass() # Permettant le masquage pendant la saisie
port = input("Entrez le port de connexion SSH (habituellement 22): ") # Port de connexion

# Utilise les mentions ci-dessus pour créer une connexion SSH
alcatel_switch_1 = {
    'device_type': 'alcatel_aos',
    'host': str(host),
    'username': str(user),
    'password': str(password),
    'port': str(port),
}

ssh1 = ConnectHandler(**alcatel_switch_1) # Se connecte en SSH


# Vérifie le mode de fonctionnement du switch, si en mode CERTIFIED, redémarre le switch, si en mode WORKING, passe à la suite
output = ssh1.send_command('show running-directory')
print(output)
if "CERTIFIED," in output:
    ssh1.send_command("reload from working no rollback", expect_string="Confirm")
    ssh1.send_command_timing("Y")
    print("Redémarrage en mode Working ...")
    exit()
if "WORKING," in output:
    print("Le switch est en mode Working.")


# Boucle permettant de dire combien de switch sont à provisionné, limitant à 4 pour le modèle 2360
nombreswitch=True
while nombreswitch:
    nb_switch = input('Combien de switch (primary+secondary compris) (1 à 4) ? ')
    if int(nb_switch) >= 1 and int(nb_switch) < 5 :
        break
    else :
        print("Seulement 4 switch peuvent être staké avec ce modèle")

# Boucle permettant de donner les numéros de VLAN Data et Voix, vérification doublon, et entre 1 et 4096.
quitterbouclevlan = 0
nombrevlanvoix=True
while nombrevlanvoix:
    if int(quitterbouclevlan) == 1:
        break
    vlan_voix = input('Numéro du VLAN Voix ? ')
    if int(vlan_voix) >= 1 and int(vlan_voix) <= 4096 :
        while True:
            vlan_data = input('Numéro du VLAN Data ? ')
            if int(vlan_data) == int(vlan_voix) :
                print("Ce vlan est déjà réserver à la voix")
                retourvlanvoix = input("Souhaitez vous changer de numéro de vlan Voix ? (o/n) : ")
                if str(retourvlanvoix) == "o":
                    break
                if str(retourvlanvoix) == "n":
                    print("")
            elif int(vlan_data) >= 1 and int(vlan_data) <= 4096 :
                quitterbouclevlan = 1
                break
            else :
                print("Vous pouvez créer uniquement un vlan entre 1 et 4096")
    else :
        print("Vous pouvez créer uniquement un vlan entre 1 et 4096")

# Assignation des ports pour chacun des switch selon les Vlans
# a faire : simplification à l'aide d'une fonction Def
if int(nb_switch) == 1: # Si 1 switchs
    nb_port_1 = input('Combien de port Voix sur le switch 1 ? (au format 1-1) ')
if int(nb_switch) == 2: # Si 2 switchs
    nb_port_1 = input('Combien de port Voix sur le switch 1 ? (au format 1-1) ')
    nb_port_2 = input('Combien de port Voix sur le switch 2 ? (au format 1-1) ')
if int(nb_switch) == 3: # Si 3 switchs
    nb_port_1 = input('Combien de port Voix sur le switch 1 ? (au format 1-1) ')
    nb_port_2 = input('Combien de port Voix sur le switch 2 ? (au format 1-1) ')
    nb_port_3 = input('Combien de port Voix sur le switch 3 ? (au format 1-1) ')
if int(nb_switch) == 4: # Si 4 switchs
    nb_port_1 = input('Combien de port Voix sur le switch 1 ? (au format 1-1) ')
    nb_port_2 = input('Combien de port Voix sur le switch 2 ? (au format 1-1) ')
    nb_port_3 = input('Combien de port Voix sur le switch 3 ? (au format 1-1) ')
    nb_port_4 = input('Combien de port Voix sur le switch 4 ? (au format 1-1) ')
if int(nb_switch) == 1:
    nb_ipbx_1 = input('Quel port sur le vlan voix (ipbx+pc) sur le switch 1 ? (au format 1-1) ')
if int(nb_switch) == 2:
    nb_ipbx_1 = input('Quel port sur le vlan voix (ipbx+pc) sur le switch 1 ? (au format 1-1) ')
    nb_ipbx_2 = input('Quel port sur le vlan voix (ipbx+pc) sur le switch 2 ? (au format 1-1) ')
if int(nb_switch) == 3:
    nb_ipbx_1 = input('Quel port sur le vlan voix (ipbx+pc) sur le switch 1 ? (au format 1-1) ')
    nb_ipbx_2 = input('Quel port sur le vlan voix (ipbx+pc) sur le switch 2 ? (au format 1-1) ')
    nb_ipbx_3 = input('Quel port sur le vlan voix (ipbx+pc) sur le switch 3 ? (au format 1-1) ')
if int(nb_switch) == 4:
    nb_ipbx_1 = input('Quel port sur le vlan voix (ipbx+pc) sur le switch 1 ? (au format 1-1) ')
    nb_ipbx_2 = input('Quel port sur le vlan voix (ipbx+pc) sur le switch 2 ? (au format 1-1) ')
    nb_ipbx_3 = input('Quel port sur le vlan voix (ipbx+pc) sur le switch 3 ? (au format 1-1) ')
    nb_ipbx_4 = input('Quel port sur le vlan voix (ipbx+pc) sur le switch 4 ? (au format 1-1) ')
if int(nb_switch) == 1:
    nb_info_1 = input('Quel port sur le vlan data (informatique) sur le switch 1 ? (au format 1-1) ')
if int(nb_switch) == 2:
    nb_info_1 = input('Quel port sur le vlan data (informatique) sur le switch 1 ? (au format 1-1) ')
    nb_info_2 = input('Quel port sur le vlan data (informatique) sur le switch 2 ? (au format 1-1) ')
if int(nb_switch) == 3:
    nb_info_1 = input('Quel port sur le vlan data (informatique) sur le switch 1 ? (au format 1-1) ')
    nb_info_2 = input('Quel port sur le vlan data (informatique) sur le switch 2 ? (au format 1-1) ')
    nb_info_3 = input('Quel port sur le vlan data (informatique) sur le switch 3 ? (au format 1-1) ')
if int(nb_switch) == 4:
    nb_info_1 = input('Quel port sur le vlan data (informatique) sur le switch 1 ? (au format 1-1) ')
    nb_info_2 = input('Quel port sur le vlan data (informatique) sur le switch 2 ? (au format 1-1) ')
    nb_info_3 = input('Quel port sur le vlan data (informatique) sur le switch 3 ? (au format 1-1) ')
    nb_info_4 = input('Quel port sur le vlan data (informatique) sur le switch 4 ? (au format 1-1) ')

# créer le VLAN Voix
cmd = "vlan "
cmd2 = " name VOICE"
result = ssh1.send_command(str(cmd)+str(vlan_voix)+str(cmd2))
print(result)

# créer le VLAN Data
cmd = "vlan "
cmd2 = " name DATA"
result = ssh1.send_command(str(cmd+vlan_data+cmd2))
print(result)

# tagué les ports en fonction du nombre de switch et du numéro de vlan VOIX
if int(nb_switch) == 1:
    nb_port = nb_port_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " tagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)

if int(nb_switch) == 2:
    nb_port = nb_port_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " tagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_port_2
    cmd = "vlan "
    cmd2 = " members port 2/1/"
    cmd3 = " tagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)

if int(nb_switch) == 3:
    nb_port = nb_port_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " tagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_port_2
    cmd = "vlan "
    cmd2 = " members port 2/1/"
    cmd3 = " tagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_port_3
    cmd = "vlan "
    cmd2 = " members port 3/1/"
    cmd3 = " tagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)

if int(nb_switch) == 4:
    nb_port = nb_port_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " tagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_port_2
    cmd = "vlan "
    cmd2 = " members port 2/1/"
    cmd3 = " tagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_port_3
    cmd = "vlan "
    cmd2 = " members port 3/1/"
    cmd3 = " tagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_port_4
    cmd = "vlan "
    cmd2 = " members port 4/1/"
    cmd3 = " tagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)

# Untagué les ports en fonction du nombre de switch et du numéro de vlan VOIX pour l'IPBX
if int(nb_switch) == 1:
    nb_port = nb_ipbx_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)

if int(nb_switch) == 2:
    nb_port = nb_ipbx_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_ipbx_2
    cmd = "vlan "
    cmd2 = " members port 2/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)

if int(nb_switch) == 3:
    nb_port = nb_ipbx_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_ipbx_2
    cmd = "vlan "
    cmd2 = " members port 2/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_ipbx_3
    cmd = "vlan "
    cmd2 = " members port 3/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)

if int(nb_switch) == 4:
    nb_port = nb_ipbx_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_ipbx_2
    cmd = "vlan "
    cmd2 = " members port 2/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_ipbx_3
    cmd = "vlan "
    cmd2 = " members port 3/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_ipbx_4
    cmd = "vlan "
    cmd2 = " members port 4/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_voix+cmd2+nb_port+cmd3))
    print(result)

# Untagué les ports en fonction du nombre de switch et du numéro de vlan Data
if int(nb_switch) == 1:
    nb_port = nb_info_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_data+cmd2+nb_port+cmd3))
    print(result)

if int(nb_switch) == 2:
    nb_port = nb_info_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_data+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_info_2
    cmd = "vlan "
    cmd2 = " members port 2/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_data+cmd2+nb_port+cmd3))
    print(result)

if int(nb_switch) == 3:
    nb_port = nb_info_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_data+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_info_2
    cmd = "vlan "
    cmd2 = " members port 2/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_data+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_info_3
    cmd = "vlan "
    cmd2 = " members port 3/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_data+cmd2+nb_port+cmd3))
    print(result)

if int(nb_switch) == 4:
    nb_port = nb_info_1
    cmd = "vlan "
    cmd2 = " members port 1/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_data+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_info_2
    cmd = "vlan "
    cmd2 = " members port 2/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_data+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_info_3
    cmd = "vlan "
    cmd2 = " members port 3/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_data+cmd2+nb_port+cmd3))
    print(result)
    nb_port = nb_info_4
    cmd = "vlan "
    cmd2 = " members port 4/1/"
    cmd3 = " untagged"
    result = ssh1.send_command(str(cmd+vlan_data+cmd2+nb_port+cmd3))
    print(result)

# Créer le provisioning des téléphones
cmd = "lldp network-policy 1 application voice vlan "
cmd2 = " l2-priority 5 dscp 46"
result = ssh1.send_command(str(cmd+vlan_voix+cmd2))
print(result)
cmd = "lldp nearest-bridge chassis tlv management port-description enable system-name enable system-description enable"
result = ssh1.send_command(str(cmd))
print(result)
cmd = "lldp nearest-bridge chassis tlv management management-address enable"
result = ssh1.send_command(str(cmd))
print(result)
cmd = "lldp nearest-bridge chassis tlv med network-policy enable"
result = ssh1.send_command(str(cmd))
print(result)
cmd = "lldp chassis med network-policy 1"
result = ssh1.send_command(str(cmd))
print(result)

# Désactive la webinterface, la connexion SSH et FTP.
output = ssh1.send_command('no aaa authentication http')
print(output)
output = ssh1.send_command('no aaa authentication ssh')
print(output)
output = ssh1.send_command('no aaa authentication ftp')
print(output)

# Enregistre la configuration à la fin du script, un délais de 120 secondes (read_timeout) est ajouté, par défaut 10 secondes, et la commande pouvant prendre jusqu'à 
# 2 minutes pour se terminer sans que Netmiko ne termine la connexion.
print("Enregistrement de la nouvelle configuration veuillez patienter... (2 minutes maxi)")
output = ssh1.send_command('write memory')
print(output)
time.sleep(3)
output = ssh1.send_command('copy running certified', read_timeout=120)
print(output)

print('Enregistré!')

ssh1.disconnect() # Déconnexion SSH
