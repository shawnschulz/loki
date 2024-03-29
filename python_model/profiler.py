import cProfile
import pstats
import ask_mistral

cProfile.run('ask_mistral.main()', 'restats')
p = pstats.Stats('restats')
p.sort_stats('cumulative').print_stats(30)
