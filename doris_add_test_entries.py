from doris.models.entry_model import Entry
import json
import requests


e1 = Entry(tags=("test", "fake", "practice", "joke"), project_tags=("doris", "geraldine"),
                          body="A manager, a mechanical engineer, and software analyst are driving back from "
                               "convention through the mountains. Suddenly, as they crest a hill, the brakes on "
                               "the car go out and they fly careening down the mountain. After scraping against "
                               "numerous guardrails, they come to a stop in the ditch. Everyone gets out of the "
                               "car to assess the damage. The manager says, 'Let's form a group to collaborate "
                               "ideas on how we can solve this issue.' The mechanical engineer suggests, "
                               "'We should disassemble the car and analyze each part for failure.' The software "
                               "analyst says, 'Let's push it back up the hill and see if it does it again.'",
                          type="entry",
                          user="dhileas", date="2020-12-09", version=0)

resp = e1.create()
print(resp.text)



e2 = Entry(tags=("test", "practice", "joke"), project_tags=("doris", "geraldine"),
                          body="A guy walks into a bar and asks for 1.4 root beers. The bartender says 'I'll have to "
                               "charge you extra, that's a root beer float'. The guy says 'In that case, better make "
                               "it a double.'", type="entry",
                          user="dhileas", date="2020-12-09", version=0)

resp2 = e2.create()
print(resp2.text)

e3 = Entry(tags=("test", "fake", "practice", "joke"), project_tags=("doris", "horatio"),
                          body="Q: How many programmers does it take to screw in a light bulb? A: None. It's a "
                               "hardware problem.", type="entry",
                          user="dhileas", date="2020-12-09", version=0)
resp3 = e3.create()
print(resp3.text)

e4 = Entry(tags=("test", "practice", "joke"), project_tags=("doris"),
                          body="In order to understand recursion you must first understand recursion.", type="entry",
                          user="dhileas", date="2020-12-09", version=0)

resp4 = e4.create()
print(resp4.text)
