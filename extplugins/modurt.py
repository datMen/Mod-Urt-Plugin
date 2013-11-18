__version__ = '2.0'
__author__  = 'LouK' # www.sniperjum.com

import b3, re, random
import b3.events
import b3.plugin
    
class Status:
    fly                  = True
    god                 = True
    
class ModurtPlugin(b3.plugin.Plugin):
    _clientvar_name = 'status_info'
    
    def onStartup(self):
        self._adminPlugin = self.console.getPlugin('admin')
     
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return
        
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self.getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)
        
    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None
           
    def findWeapid(self, weapon):
        if (weapon == "sr8") or (weapon == "SR8"):
            valor = "N"
        elif (weapon == "spas") or (weapon == "SPAS") or (weapon == "FRANCHI") or (weapon == "franchi"):
            valor = "D"
        elif (weapon == "mp5") or (weapon == "MP5") or (weapon == "MP5K") or (weapon == "mp5k"): 
            valor = "E"
        elif (weapon == "ump") or (weapon == "UMP") or (weapon == "UMP45") or (weapon == "ump45"):
            valor = "F"
        elif (weapon == "HK69") or (weapon == "hk69") or (weapon == "hk") or (weapon == "HK"):
            valor = "G"
        elif (weapon == "lr300") or (weapon == "LR300") or (weapon == "LR") or (weapon == "lr"):
            valor = "H"
        elif (weapon == "PSG") or (weapon == "psg") or (weapon == "PSG1") or (weapon == "psg1"):
            valor = "J"
        elif (weapon == "g36") or (weapon == "G36"):
            valor = "I"
        elif (weapon == "ak") or (weapon == "AK") or (weapon == "AK103") or (weapon == "ak103"):
            valor = "O"
        elif (weapon == "NEGEV") or (weapon == "negev") or (weapon == "NE") or (weapon == "ne"):
            valor = "Q"
        elif (weapon == "M4") or (weapon == "m4") or (weapon == "m4a") or (weapon == "M4A"):
            valor = "S"
        elif (weapon == "grenade") or (weapon == "GRENADE") or (weapon == "HE") or (weapon == "he"):
            valor = "K"
        elif (weapon == "SMOKE") or (weapon == "smoke") or (weapon == "SM") or (weapon == "sm"):
            valor = "M"
        elif (weapon == "KNIFE") or (weapon == "knife") or (weapon == "KN") or (weapon == "kn"):
            valor = "A"
        else:
            client.message("Couldn't find: ^2%s" % weapon)
            return False
        return valor
    
    def findItemid(self, weapon):
        if (weapon == "kevlar") or (weapon == "KEVLAR") or (weapon == "KEV") or (weapon == "kev"):
            valor = "A"
        elif (weapon == "helmet") or (weapon == "HELMET") or (weapon == "HEL") or (weapon == "hel"):
            valor = "F"
        elif (weapon == "medkit") or (weapon == "MEDKIT") or (weapon == "MEDIC") or (weapon == "medic") or (weapon == "MED") or (weapon == "med"):
            valor = "C"
        elif (weapon == "TAC") or (weapon == "tac") or (weapon == "nvg") or (weapon == "NVG") or (weapon == "goggles") or (weapon == "TacGoggles") or (weapon == "tacgoggles"):
            valor = "B"
        elif (weapon == "SIL") or (weapon == "sil") or (weapon == "silencer") or (weapon == "SILENCER"):
            valor = "D"
        elif (weapon == "LAS") or (weapon == "las") or (weapon == "laser") or (weapon == "LASER"):
            valor = "E"
        else:
            client.message("Couldn't find: ^2%s" % weapon)
            return False
        return valor
    
    def get_status(self, client):
        if not client.isvar(self, self._clientvar_name):
            client.setvar(self, self._clientvar_name, Status())
            
        return client.var(self, self._clientvar_name).value
           
    def cmd_giveweapon(self, data, client, cmd=None):
        """\
        Give weapon to a player.
        """
        if not data:
            client.message('Correct usage is ^2!gw ^4<playername or partialname> <weapon> <amount>')
            return False
        input = self._adminPlugin.parseUserCmd(data)
        input = data.split()
        cname = input[0]
        sclient = self._adminPlugin.findClientPrompt(cname, client)
        
        if len(input) == 2:
            weapon = input[1]
        elif len(input) == 3:
            weapon = input[1]
            amount = input[2]
        elif len(input) == 4:
            weapon = input[1]
            amount = input[2]
            shells = input[3]
        if not sclient:
            weapon = input[0]
            if len(input) == 2:
                amount = input[1]
            elif len(input) == 3:
                amount = input[1]
                shells = input[2]
            if not weapon:
                client.message('Correct usage is ^2!gw ^4<playername or partialname> <weapon> <amount>')
                return False
            
            if len(input) == 3:
                self.console.write('gw %s %s %s %s' % (client.cid, self.findWeapid(weapon), amount, shells))
                client.message("You have now a ^2%s^7 with ^5%s^7 bullets and ^5%s^7 shells" % (weapon, amount, shells))
            elif len(input) == 2:
                self.console.write('gw %s %s %s' % (client.cid, self.findWeapid(weapon), amount))
                client.message("You have now a ^2%s^7 with ^5%s^7 bullets" % (weapon, amount))
            else:
                self.console.write('gw %s %s' % (client.cid, self.findWeapid(weapon)))
                client.message("You have now a ^2%s" % weapon)
            return False
        
        if len(input) == 2:
            self.console.write('gw %s %s' % (sclient.cid, self.findWeapid(weapon)))
            sclient.message("%s gave you a ^2%s" % (client.exactName, weapon))
            client.message("You gave a ^2%s ^7to %s" % (weapon, sclient.exactName))
        elif len(input) == 3:
            self.console.write('gw %s %s %s' % (client.cid, self.findWeapid(weapon), amount))
            sclient.message("%s gave you a ^2%s^7 with ^5%s^7 bullets" % (client.exactName, weapon, amount))
            client.message("You gave a ^2%s^7 with ^5%s^7 bullets ^7to %s" % (weapon, amount, sclient.exactName))
        elif len(input) == 4:
            self.console.write('gw %s %s %s %s' % (client.cid, self.findWeapid(weapon), amount, shells))
            sclient.message("%s gave you a ^2%s^7 with ^5%s^7 bullets and ^5%s^7 shells" % (client.exactName, weapon, amount, shells))
            client.message("You gave a ^2%s^7 with ^5%s^7 bullets and ^5%s^7 shells to %s" % (weapon, amount, shells, sclient.exactName))
            
    def cmd_giveitem(self, data, client, cmd=None):
        """\
        Give an item to a player.
        """
        if not data:
            client.message('Correct usage is ^2!gi ^4<playername or partialname> <item>')
            return False
        
        input = self._adminPlugin.parseUserCmd(data)
        input = data.split()
        cname = input[0]
        sclient = self._adminPlugin.findClientPrompt(cname, client)
        
        if len(input) == 2:
            item = input[1]
        if not sclient:
            item = input[0]
            if not item:
                client.message('Correct usage is ^2!gi ^4<playername or partialname> <item>')
                return False
            
            self.console.write('gi %s %s' % (client.cid, self.findItemid(item)))
            client.message("You have now a ^2%s" % item)
            return False
        
        if not item:
            client.message('Correct usage is ^2!gi ^4<playername or partialname> <item>')
            return False
        
        self.console.write('gi %s %s' % (sclient.cid, self.findItemid(item)))
        sclient.message("%s gave you a ^2%s" % (client.exactName, item))
        client.message("You gave a ^2%s ^7to %s" % (item, sclient.exactName))
            
    def cmd_health(self, data, client, cmd=None):
        """\
        Give health to a player.
        """
        if not data:
            self.console.write('gh %s 100' % (client.cid))
            client.message("Health ^2Restored")
            return False
            
        input = self._adminPlugin.parseUserCmd(data)
        scname = input[0]
        sclient = self._adminPlugin.findClientPrompt(scname, client)
        if len(input) == 2:
            amount = input[1]
        if not sclient:
            amount = input[0]
                
            self.console.write('gh %s %s' % (client.cid, amount))
            client.message('Health ^2+%s' % amount)
            return False
        
        if not amount:
            self.console.write('gh %s 100' % (sclient.cid))
            sclient.message("%s ^2Restored ^7your Health" % client.exactName)
            client.message("You ^2Restored ^7%s's Health" % sclient.exactName)
        else:
            self.console.write('gh %s %s' % (client.cid, amount))
            sclient.message("%s Gave you ^2+%s ^7Hps" % (client.exactName, amount))
            client.message("You Gave ^2+%s ^7Hps to %s" % (amount, sclient.exactName))
        
    def cmd_invisible(self, data, client=None, cmd=None):
        if not data:
            self.console.write('invisible %s' % (client.cid))
            self.console.write('sendclientcommand %s cp "You are ^4Invisible!!"' % (client.cid))
            client.message("Type ^2!vis ^7to make you visible")
            return False
        
        input = self._adminPlugin.parseUserCmd(data)
        scname = input[0]
        sclient = self._adminPlugin.findClientPrompt(scname, client)
        self.console.write('invisible %s' % (sclient.cid))
        self.console.write('sendclientcommand all print "%s ^7is now ^4Invisible^7!!!"' % (sclient.exactName))
        self.console.write('sendclientcommand %s cp "You are ^4Invisible!!"' % (sclient.cid))
        client.message("Type ^2!vis ^7to make %s visible" % sclient.exactName)
        
    def cmd_visible(self, data, client=None, cmd=None):
        if not data:
            self.console.write('forcecvar %s cg_rgb "1"' % (client.cid))
            self.console.write('forcecvar %s cg_rgb "0"' % (client.cid))
            self.console.write('sendclientcommand %s cp "You are now ^2visible^7!!"' % (client.cid))
            return False
            
        input = self._adminPlugin.parseUserCmd(data)
        scname = input[0]
        sclient = self._adminPlugin.findClientPrompt(scname, client)
        self.console.write('forcecvar %s cg_rgb "1"' % (sclient.cid))
        self.console.write('forcecvar %s cg_rgb "0"' % (sclient.cid))
        self.console.write('sendclientcommand all print "%s ^7is now ^2Visible"' % (sclient.exactName))
        self.console.write('sendclientcommand %s cp "You are now ^2Visible^7!!"' % (sclient.cid))
            
    def cmd_kill(self, data, client, cmd=None):
        """\
        Kill yourself or kill a player.
        """
        input = self._adminPlugin.parseUserCmd(data)
        if not data:
            self.console.write("kill %s" % (client.cid))
            client.message('^7You are ^1DEAD')
            return False
        
        scname = input[0]
        sclient = self._adminPlugin.findClientPrompt(scname, client)
        self.console.write('kill %s' % (sclient.cid))
        client.message('You ^1KILLED ^7%s' % sclient.exactName)
        
    def cmd_fly(self, data, client, cmd=None):
        """\
        Add bots to the server
        """
        Status = self.get_status(client)
        if not data:
            if Status.fly:
                self.console.write("sv_cheats 1")
                self.console.write("spoof %s noclip" % (client.cid))
                self.console.write("sv_cheats 0")
                self.console.write('sendclientcommand %s cp "^5Fly ^7little bird, ^5Fly^7!!"' % (client.cid))
                Status.fly = False
            else:
                self.console.write("sv_cheats 1")
                self.console.write("spoof %s noclip" % (client.cid))
                self.console.write("sv_cheats 0")
                self.console.write('sendclientcommand %s cp "You have returned to ^3Earth"' % (client.cid))
                Status.fly = True
            return False
                
        input = self._adminPlugin.parseUserCmd(data)
        scname = input[0]
        sclient = self._adminPlugin.findClientPrompt(scname, client)
        if Status.fly:
            self.console.write("sv_cheats 1")
            self.console.write("spoof %s noclip" % (sclient.cid))
            self.console.write("sv_cheats 0")
            self.console.write('sendclientcommand %s cp "^5Fly ^7little bird, ^5Fly^7!!"' % (sclient.cid))
            client.message('%s is ^5Flying' % sclient.exactName)
            Status.fly = False
        else:
            self.console.write("sv_cheats 1")
            self.console.write("spoof %s noclip" % (sclient.cid))
            self.console.write("sv_cheats 0")
            self.console.write('sendclientcommand %s cp "You have returned to ^3Earth"' % (sclient.cid))
            client.message('%s is not flying anymore' % sclient.exactName)
            Status.fly = True
    
    def cmd_god(self, data, client, cmd=None):
        Status = self.get_status(client)
        if not data:
            if Status.god:
                self.console.write("sv_cheats 1")
                self.console.write("spoof %s god" % (client.cid))
                self.console.write("sv_cheats 0")
                self.console.write('sendclientcommand %s cp "You are now a ^6GoD"' % (client.cid))
                Status.god = False
            else:
                self.console.write("sv_cheats 1")
                self.console.write("spoof %s god" % (client.cid))
                self.console.write("sv_cheats 0")
                self.console.write('sendclientcommand %s cp "You are now a ^3Mortal"' % (client.cid))
                Status.god = True
            return False
                
        input = self._adminPlugin.parseUserCmd(data)
        scname = input[0]
        sclient = self._adminPlugin.findClientPrompt(scname, client)
        if Status.god:
            self.console.write("sv_cheats 1")
            self.console.write("spoof %s god" % (sclient.cid))
            self.console.write("sv_cheats 0")
            self.console.write('sendclientcommand %s cp "You are now a ^6GoD"' % (sclient.cid))
            client.message('%s is in ^6GoD ^7mode' % sclient.exactName)
            Status.god = False
        else:
            self.console.write("sv_cheats 1")
            self.console.write("spoof %s god" % (sclient.cid))
            self.console.write("sv_cheats 0")
            self.console.write('sendclientcommand %s cp "You are now a ^3Mortal"' % (sclient.cid))
            client.message('%s is now a ^6Mortal' % sclient.exactName)
            Status.god = True
        
    def cmd_teleport(self, data, client, cmd=None):
        input = self._adminPlugin.parseUserCmd(data)
        if not data:
            client.message('Correct usage is ^2!teleport ^4<playername or partialname> <playername or partialname>')
            return False
        
        scname = input[0]
        ccname = input[1]
        sclient = self._adminPlugin.findClientPrompt(scname, client)
        if not ccname:
            self.console.write("teleport %s %s" % (client.cid, sclient.cid))
        else:
            cclient = self._adminPlugin.findClientPrompt(ccname, client)
            self.console.write("teleport %s %s" % (sclient.cid, cclient.cid))