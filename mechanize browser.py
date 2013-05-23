#!/usr/bin/env python
import mechanize
import cookielib

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)


# User-Agent 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#setting up proxy for iitb
# Proxy and user/password
br.set_proxies({"http": "username:password@netmon.iitb.ac.in:80"})

# Proxy
br.set_proxies({"http": "netmon.iitb.ac.in:80"})
# Proxy password
br.add_proxy_password("username", "password")