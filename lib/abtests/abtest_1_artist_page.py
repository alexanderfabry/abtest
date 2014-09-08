
from lib.mixpanel_test import MixpanelTest

mp = MixpanelTest()
data = mp.request(
	funnel_id=809349,
	seg_property='artist-page-interface',
	from_date='2014-08-28'
)
mp.test(data, control='fillwidth', variations=['filter', 'filter_carousel'])
