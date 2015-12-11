akamai_refresh
================

Just a simple script to refresh Akamai Cache

Note: Configure credentials in akamai_creds.py before using

# Refresh a URL
	python akamai_refresh.py -u http://www.foobar.org

# Refresh a CPCODE
	python akamai_refresh.py -c CPCODE
	
# Additional options
	type:
		-t remove or invalidate (default it invalidate)
	domain:
		-D staging or production (default is production)


# Documentation	

	https://api.ccu.akamai.com/ccu/v2/docs/index.html
