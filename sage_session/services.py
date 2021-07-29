from django.contrib.gis.geoip2 import GeoIP2

from user_agents import parse


def analyse_user_agent(user_agent):
    """Analyse user agent string and extract information
    :param user_agent: user agent string
    :type user_agent: str
    :return: information about user device and etc
    :rtype: tuple (
        device brand,
        device model,
        browser,
        browser version,
        os,
        os version,
        is mobile,
        is tablet,
        is touch capable,
        is pc,
        is bot
    )
    """
    agent = parse(user_agent)
    return (
        agent.device.brand,
        agent.device.model,
        agent.browser.family,
        agent.browser.version_string,
        agent.os.family,
        agent.os.version_string,
        agent.is_mobile,
        agent.is_tablet,
        agent.is_touch_capable,
        agent.is_pc,
        agent.is_bot
    )


def get_ip_location(ip):
    """Get location information of ip
    :param ip: IP address
    :type ip: str
    :return: city & country of the ip address
    :rtype: tuple (country, city)
    """
    g = GeoIP2()
    data = g.city(ip)
    return (
        data.get('country_name'),
        data.get('city')
    )
