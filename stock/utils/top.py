from nsetools import Nse
import os
#os.environ['http_proxy'] = "http://142051002:ayyappa18@172.18.61.10:3128"
#os.environ['https_proxy'] = "http://142051002:ayyappa18@172.18.61.10:3128"

nse = Nse()


def top_gainers():
    top_gainers = nse.get_top_gainers()
    return top_gainers


def top_losers():
    top_losers = nse.get_top_losers()
    return top_losers


def main():
    top_gainers()
    top_losers()

if __name__ == '__main__':
    main()
