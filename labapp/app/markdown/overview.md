<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/arch.png" width="300px" height="auto" alt="arch">
</div>

# **Overview**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

The lab environment, it's apps, and method of interaction are intentionally simple in an attempt to streamline...

<div style="height:25px"></div>

## **Architecture**

The lab environment contains three distributed sites meshed using the F5 Distributed Cloud Global Network.

<div style="height:25px"></div>

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/mcnp-aws.png" width="auto" height="30px"> &nbsp;&nbsp;
    <strong>student-awsnet</strong> in Amazon Web Services
  </li>
  <li class="list-group-item">
  <img src="/static/mcnp-azure.png" width="auto" height="30px"> &nbsp;&nbsp;&nbsp;
  <strong>student-azurenet</strong> in Microsoft Azure
  </li>
  <li class="list-group-item">
  <img src="/static/mcnp-udf.png" width="auto" height="30px"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <strong>Lab CE</strong> in UDF 
  </li>
</ul>

<div style="height:25px"></div>

<img src="/static/mcn-prac-arch-base.png" width="auto" height="600px" alt="Arch diagram">

## **Cloud App**

An instance of the [cloud app](https://github.com/f5devcentral/f5xc-lab-mcn-practical/tree/main/cloudapp) is hosted in each cloud site.
The [cloud app](https://github.com/f5devcentral/f5xc-lab-mcn-practical/tree/main/cloudapp) is a simple application that echoes back an HTTP request.
Remember while working through the lab, unless otherwise noted, the tests are displaying the headers and info **from the request received by the app**.

<div style="height:25px"></div>

## **Lab Exercises**

To complete the lab exercises, you will interact with a load balancer advertised from the Customer Edge in your UDF site from the [lab app](https://github.com/f5devcentral/f5xc-lab-mcn-practical/tree/main/labapp).

Test button



```http
GET https://eph-ns.mcn-lab.f5demos.com/ HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "env": "Azure",
  "info": {
    "method": "GET",
    "path": "/",
    "url": "https://eph-ns.mcn-lab.f5demos.com"
  },
  "request_headers": {
    "Host": "https://eph-ns.mcn-lab.f5demos.com",
    "User-Agent": "curl/8.4.0",
    "X-Request-Id": "9cff4a3d-29e1-458e-b62e-3192e8398e14"
  }
}
```


``curl`` and ``jq`` are provided on the UDF "Runner" instance. 

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

Next, visit the <strong><a href="/setup" >setup page</a></strong> before starting the exercises.






