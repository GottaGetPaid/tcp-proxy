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

I'm unfamiliar with the python standard libraries, so I watched this helpful tutorial: https://youtu.be/3QiPPX-KeSc?si=BRabx8Pf4wc9MOlj

Then with lots of help from Perplexity, I made the basic structure for my TCP proxy and a testing suite for it.

Unfortunately, I this is as far as I'm getting. I was caught up by a few other projects and a final tomorrow so I didn't have much time to spend on the TCP proxy :p. If I had more time to work on this project though, I would test to make sure it works with different services like FTP, and also try making something to automatically detect the optimal buffer size to use, rather than a constant value.

Thanks for giving me the opportunity to learn more about networking and considering me for your internship position!

