# block_kit

This library allow functional creation of Block Kit (Slack) messages:

```
from block_kit import *
import json

print(json.dumps(
    message(
        "test",
        blocks(
            header(
                plain_text('test'),
            ),
            section(
                plain_text('test'),
            ),
            section(
                fields(
                    markdown('test'), 
                ),
            ),
            image(image_url='test'),
            actions(
                button(text=plain_text("Create case"), action="click_me_123", action_id="actionId-0", value="click me")
            ),
        ),
    ), cls=BlockKitEncoder)
 )
 ```

# Creator

[DTACT](https://dtact.com/)

# Copyright and license

Code and documentation copyright 2011-2021 DTACT.

Code released under the Apache license.
