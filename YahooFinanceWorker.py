import requests
import threading
import time
from bs4 import BeautifulSoup


class YahooFinancePriceWorker(threading.Thread):
    def __init__(self, symbol, **kwargs):
        super(YahooFinancePriceWorker, self).__init__(**kwargs)
        self._price = None
        self._symbol = symbol
        base_url = "https://uk.finance.yahoo.com/quote/"
        self._url = '{0}{1}'.format(base_url, self._symbol)
        self.start()

    def get_price(self):
        return self._price

    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': 'F=d=V8WZlmc9vJjXtalE7mMJ_JaJv6aqmAQLWf4_p2Pb3A--; PH=l=en-GB; Y=v=1&n=2jo4kuabpce2a&l=0h30l0drtwx/o&p=m2ovvuk00000000&ig=0pkq3&iz=LA14RG&r=8s&intl=uk; OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiTVhNQlY1TlhRVlQyVTdTSUlRRU5PM05UVkUiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJIV01UNXBxY1MwU3MifX0.vNRje4t36rWX0MrM1gvS9Fwa5z_UZi_gRQod-CErI2K8eBQnPjm9e8tSRW76i3rZK0aPF-KXjpkcG9iiMPr90iaPsrOtmMXN576DOOZ6U4roYcJvNyLBiKvWqHtzLfLOXA9dVRBCjICDP_IeIbLGEn4YWhkexbj07evJXgWLthg; T=af=QXdBQjFDQXpBQlJSJnRzPTE2OTIxMzEyNDcmcHM9QzREYS5wN0NMeVBhOU5HdUo0N3l5US0t&d=bnMBeWFob28BZwFNWE1CVjVOWFFWVDJVN1NJSVFFTk8zTlRWRQFhYwFBT1MxREVrTwFhbAFhcmRhdmFuMTM2NwFzYwFkZXNrdG9wX3dlYgFmcwFEYTRKcmlOa3NvQjUBenoBdi45MmtCQTdFAWEBUUFFAWxhdAF2Ljkya0IBbnUBMA--&kt=EAAr7PMuRdtyRBhrnv1Bqf5qg--~I&ku=FAADPry5iAQ_IyhRiDzO8phe9v_qlKcNK2rjKawCG5R28UrwQK_bfhdcpuCHBy6t0P4NuZlScAnmKEOqA68NTv5oHSrBjCEwhMFZX19YZa_4CJJ1Auc.ELIwx.WJPFFaXreUAhZUDzcH7_iaiwig8I.he.3o8DvJISNCX9GT9rtlsQ-~E; GUCS=ARGj_iPx; GUC=AQABCAFlIb5lTEIgVQR4&s=AQAAADBY7lvj&g=ZSBwqg; A1=d=AQABBHmAsmQCEJvACbIMlnU7ru5AFpTxuMAFEgABCAG-IWVMZfbPb2UB_qMBAAcIeYCyZLwQKycID0-RVfl58lT0kCzQ8gwuGQkBBwoBlA&S=AQAAAuXbz-Phe7qfegPUMpH1Rr4; A3=d=AQABBHmAsmQCEJvACbIMlnU7ru5AFpTxuMAFEgABCAG-IWVMZfbPb2UB_qMBAAcIeYCyZLwQKycID0-RVfl58lT0kCzQ8gwuGQkBBwoBlA&S=AQAAAuXbz-Phe7qfegPUMpH1Rr4; A1S=d=AQABBHmAsmQCEJvACbIMlnU7ru5AFpTxuMAFEgABCAG-IWVMZfbPb2UB_qMBAAcIeYCyZLwQKycID0-RVfl58lT0kCzQ8gwuGQkBBwoBlA&S=AQAAAuXbz-Phe7qfegPUMpH1Rr4; cmp=t=1696624802&j=1&u=1---&v=97; EuConsent=CPuR2wAPuR2wAAOACBENDZCoAP_AAEfAACiQJVtB9G7WTXNncXp_YPs0eYUX1VBp4uAxBgCBA-ABzBsUIIwGVmEzJEyIJigCGAIAoEJBIEFtGAlAAFAQIIAFABHICEEAJBAAIGAAECAAAgBACBBIEwAAAAAQoUBXMhQgkAdEQFoIQchAlgAgAQIAICAEgIhBAgQAEAAgQABIAEAIgigAggAAAAIAAAAEAFAIEQBABgECAIJVgAkGrUQBNiUGBNIGEUKIEQVBABQKAAAgCBAgAADBgUIIwCVGESAEAIAAgAAAIAoAIBAAABAAhAAEAQIIAAABAIAAAAIBAAACAAEAAAAAAAAAAIAQAAAAAAIQBEAAQggAEAABAAQUAAEAAgAAAAACAEAIhAAAAAAAAgAAAAAEAIAgAAgAAAAAIAAAAAAAAIEABABgAAAIAYaADAAEQUBEAGAAIgoCoAMAARBQ; PRF=t%3DABT%252BACN'
        }
        response = requests.get(self._url, headers=headers)
        if response.status_code != 200:
            print("Couldn't get price")
            return 0
        soup = BeautifulSoup(response.text)
        price_element = soup.find(attrs={"data-test": "qsp-price"})
        self._price = price_element.attrs["value"]
