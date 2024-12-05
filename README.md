Justin Yang
## 11/30/24

### 1. Getting Started

First, I needed to understand what I'm trying to build. I reviewed the TCP/IP and OSI network models and their layers on this video: https://youtu.be/CRdL1PcherM?si=dMnGLPY4UCzL2Rt7. 

Next, I needed to figure out what network proxies were which this video helped with: https://youtu.be/4NB0NDtOwIQ?si=DhqFThDD__a7VSCP. 

I was still confused on what a TCP proxy was specifically, so I asked Perplexity "is a tcp proxy just a reverse proxy?". I had the wrong idea because apparently reverse proxies operate on layer 7 and TCP proxies operate on layer 4.

| TCP Proxy                             | Reverse Proxy                                  |
| ------------------------------------- | ---------------------------------------------- |
| Operates at transport layer (Layer 4) | Can operate at application layer (Layer 7)     |
| Primarily forwards TCP segments       | Can modify and inspect traffic                 |
| Limited to TCP protocol               | Supports multiple protocols                    |
| Basic traffic forwarding              | Advanced features like SSL encryption, caching |

This gave me a little more insight into what a TCP proxy is, but I'm still unclear. I kept asking perplexity more questions and came to the conclusion that a TCP proxy is just a program that manages TCP traffic between two computers, and does any variety of tasks with the traffic it intercepts (https://www.perplexity.ai/page/what-is-a-tcp-proxy-trk3L64lRbePJMG_DeJLMw).


## 12/4/24
### 2. Building a TCP Proxy

Now that I have a rough idea of what a TCP proxy is, I need to actually build one.

I found an article online on how to build a TCP proxy in python: https://thepythoncode.com/article/building-a-tcp-proxy-with-python#implementation, read through its explanations, and the code. 

I'm unfamiliar with the python standard libraries for networking, so I watched this helpful tutorial: https://youtu.be/3QiPPX-KeSc?si=BRabx8Pf4wc9MOlj. And also watched this short video which helped clear up what network sockets are for me: https://youtu.be/_FVvlJDQTxk?si=As96U5tOPdnifpj_ (I also realized sockets not the same as WebSockets 😅).

Then I made the basic structure for my TCP proxy and a testing suite for it with Perplexity.

To add the CLI functionality, I made a main program for the TCP proxy file as well. To add signal handling, I used python's signal, sys, and logging libraries.

After all that, I updated the test file to reflect changes made to the proxy.

Unfortunately, I this is as far as I'm getting 🥲. I was caught up by a few other projects and a final tomorrow so I didn't have much time to spend on the TCP proxy :p. 

If I had more time to work on this project though, I would: 
* Make sure I understand all the code, a lot was generated.
* Make the test suite more thorough.
* Test to make sure it works across different operating systems (although python should work everywhere).
* Try making something to automatically detect the optimal buffer size to use, rather than a constant value.
* Check if the proxy works with API calls.

Thanks for giving me the opportunity to learn more about networking and considering me for your internship position!

### 3. Instructions + Additional 
#### Instructions for running
1. Have python3 installed. 
2. Same as given instructions. i.e. 
   To run `tcp_proxy.py`: `python3 tcpproxy.py --ip 127.0.0.1 --port 5555 --server "192.168.5.2:80"` from the project root folder.
   To run `test_tcp_proxy.py`: `python3 test_tcp_proxy.py`.
#### Citations
See `citation.md`

#### Light Links
This project was made for [Light Links Inc.](https://www.linkedin.com/company/lightlinks-inc/)'s software intern assessment. Instructions can be found in `assessment.pdf`.


