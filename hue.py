"""
Created on Apr 4, 2014
Updated on May 16, 2018

@author: Dario Bonino
@author: Luigi De Russis

Copyright (c) 2014-2018 Dario Bonino and Luigi De Russis
 
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
"""

import rest
import time
from rgb_xy import Converter
from rgb_xy import GamutB

if __name__ == '__main__':
    converter = Converter(GamutB)
    print(converter.rgb_to_xy(255, 0, 0))
    # the base URL
    base_url = 'http://localhost:8000'
    # if you are using the emulator, probably the base_url will be:
    # base_url = 'http://localhost:8000'
    
    # example username, generated by following https://www.developers.meethue.com/documentation/getting-started
    username = 'newdeveloper'
    # if you are using the emulator, the username is:
    # username = 'newdeveloper'

    # lights URL
    lights_url = base_url + '/api/' + username + '/lights/'
    
    # get the Hue lights
    all_the_lights = rest.send(url=lights_url)
    print(all_the_lights)
    # for(all_the_lights)

    if type(all_the_lights) is dict:
        # iterate over the Hue lights, turn them on with the color loop effect
        for light in all_the_lights:
            url_to_call = lights_url + light + '/state'
            body = '{"on":true, "xy":[0.675, 0.322]}'
            # to set the red color
            # body = '{ "hue" : 0 }'
            # more colors: https://www.developers.meethue.com/documentation/core-concepts
            rest.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})

        # wait 10 seconds...
        to_yellow = 25.5
        for i in range(0, 10):
            time.sleep(1)
            body = str({"xy": converter.rgb_to_xy(255, to_yellow, 0)})
            print(to_yellow)
            print(body)
            for light in all_the_lights:
                url_to_call = lights_url + light + '/state'
                rest.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
            to_yellow += 25.5

        # iterate over the Hue lights and turn them off
        for light in all_the_lights:
            url_to_call = lights_url + light + '/state'
            body = '{ "transitiontime": 5,"xy":[0.4325035269415173, 0.5007488105282536] }'
            rest.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    else:
        print('Error:', all_the_lights[0]['error'])
