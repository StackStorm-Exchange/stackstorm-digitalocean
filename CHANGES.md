# Change Log

# 0.3.3

- Fix JSON serialization with recent upstream digitalocean package changes

# 0.3.2

- Version bump to fix tagging issues

# 0.3.1

- Added unit tests
  (contributed by: Nick Maludy - Encore Technologies) 
  
- Fixed a bug where `digitalocean` python module was returning custom objects instead
  of dicts/lists causing StackStorm to ignore the results. After this fix all
  objects returned from `digitaloceean` API calls should be converted into StackStorm
  friendly dicts/lists. 
  (fixed by: Nick Maludy - Encore Technologies) 
  (reported by: Casey Havenor)

# 0.3.0

- Updated action `runner_type` from `run-python` to `python-script`

# 0.2.0

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.

# 0.1.0

- First release 
