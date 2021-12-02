# Day 23: Category Six

## Problem Summary ([?](https://adventofcode.com/2019/day/23))

This problem has us chain fifty [Intcode](../day09) computers together in a network.
The computers will send packets to each other.
They will output a destination address, and then a "packet" of an x and a y to send to the computer at that address.
The computers are conceptually all running in parallel.
If they have not received a packet, their input is -1.

**Part 1** asks for the y of the first packet sent to address 255.
The answer for my input is 27061.

**Part 2** explains address 255 is the "NAT" address, essentially a register that holds a single packet.
When the computers have sent and processed all their packets, and no new packets are being sent, we say the network is idle.
When this happens we send the NAT packet as input to Computer 0.
We are tasked with finding the first duplicate NAT y value sent to Computer 0.
The answer for my input is 19406.


## Retrospective

My Intcode interpreter from previous days was _not_ designed with async execution, piping outputs, or blocking on inputs in mind.
Even my solution to [Day 7: Amplification Circuit](../day07) ([?](https://adventofcode.com/2019/day/7)) runs the computers in sequence.
For this one, to run the computers async we rely on the fact that the `input` command is to default to -1 when there's nothing to read.
When the `input` command receives a -1 we "halt" the computer, which suspends execution and allows us to move to the next tape.
After we try running all the computers until they require input, we simply start from the top and try resuming each of the computers in sequence again.

For part 2 we do essentially the same thing, but to detect network idle we ensure at least one of the computers was not waiting for input.
If we run through each computer once and none of them have outputted a new packet, we send the NAT to computer 0 as directed.

Ran into a weird quirk.
On the first run through all of the computers report nothing to send, which my code was interpretting and trying to handle as network idle.
My solution to this was to essentially do-while the deadlock check.
Instead of setting `did_work = False` at the top of the loop and setting it to `True` as we do work, I set it to `True` at the very beginning of the script and reset it to `False` only at the _end_ of the loop.
This meant on the first run we skip the deadlock check.
Semantically it's a little messy but it got me the behavior I needed.

It's pretty neat that this problem had me designing an async loop like python's, leveraging lazy generators like python does.

Placed pretty well.
Happy with this.

The first paragraph of the problem description made me laugh out loud.
I love it.
