#!/usr/bin/env python

import subprocess


magnet = "magnet:?xt=urn:btih:4d7c1fa69d9c42048622dc0eacce827fbe636d68&dn=Teen.Mom.2.S08E20.WEB.x264-CookieMonster%5Beztv%5D.mkv%5Beztv%5D&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A80&tr=udp%3A%2F%2Fglotorrents.pw%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969"
subprocess.call(["transmission-cli", "magnet:?xt=urn:btih:4d7c1fa69d9c42048622dc0eacce827fbe636d68&dn=Teen.Mom.2.S08E20.WEB.x264-CookieMonster%5Beztv%5D.mkv%5Beztv%5D&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A80&tr=udp%3A%2F%2Fglotorrents.pw%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969"])
