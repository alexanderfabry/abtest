abtest
======

Wrapper around https://github.com/bogdan-kulynych/trials to use with Mixpanel segmentation properties.

In `etc`: rename `mp.yml.sample` to `mp.yml` and include your mixpanel credentials.

In `lib/abtests`, a file like:

```python
from lib.mixpanel_test import MixpanelTest

mp = MixpanelTest()
data = mp.request(
	funnel_id=FUNNEL_ID,
	seg_property='SEGMENT_PROPERTY',
	from_date='2014-08-28'
)
mp.test(data, control='control', variations=['variation1', 'variation2'])
```
In `bin/run`: load the above file

In the terminal: `bin/run`.
