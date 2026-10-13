# homebot

Small intercom program using Discord as a backend, designed to run on a Raspberry Pi, using a USB numpad as input method. It aims to reduce the amount of yelling inside the house :).

Flow:
1) The raspberry user inputs a command using the numpad. Commands consist of a pre-defined list of adressees and actions
    * E.g. entering 1 will notify everyone of dinner, 2 will only notify user1, 4 will notify everyone that 'we need to leave', etc
2) This the command is translated into a message and send to a discord group with both recipients in it
3) To provide feedback about whether the message was received by the recipient(s), the numpad's numlock led indicator is used. Depending on who responded to the message, the led indicator will start blinking at different frequencies.