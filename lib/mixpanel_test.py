import datetime
import yaml
from trials import Trials
from mixpanel import Mixpanel


class MixpanelTest(object):

	def __init__(self):
		with open('etc/mp.yml', 'r') as f:
			mp = yaml.load(f)
		self.api = Mixpanel(
			api_key=mp['api_key'],
			api_secret=mp['api_secret']
		)

	def request(self, funnel_id, seg_property, from_date):
		data = self.api.request(['funnels'], {
			'funnel_id': funnel_id,
			'on': 'properties["%s"]' % seg_property,
			'from_date': from_date,
			'to_date': datetime.date.today().isoformat(),
			'interval': 60
		})['data']

		return data[from_date]

	def test(self, data, control, variations):
		update = {}
		buckets = [control] + variations
		for bucket in buckets:
			total = data[bucket][0]['count']
			successes = data[bucket][1]['count']
			update[bucket] = (successes, total - successes)

		test = Trials(buckets)
		test.update(update)

		dominances = test.evaluate('dominance', control=control)
		lifts = test.evaluate('expected lift', control=control)
		intervals = test.evaluate('lift CI', control=control, level=95)

		for variation in variations:
			print('Variation {name}:'.format(name=variation))
			s, t = update[variation]
			print('* Successes: {0}, Total: {1}, Percent: {2:2.3f}%'.format(s, t, 100*float(s)/t))
			print('* E[lift] = {value:.2%}'.format(value=lifts[variation]))
			print('* P({lower:.2%} < lift < {upper:.2%}) = 95%'.format(lower=intervals[variation][0], upper=intervals[variation][2]))
			print('* P({name} > {control}) = {value:.2%}'.format(name=variation, control=control, value=dominances[variation]))
			print
