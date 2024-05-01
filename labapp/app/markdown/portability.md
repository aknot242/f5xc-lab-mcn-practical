<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/manip.png" width="300px" height="auto" alt="intro">
</div>

# **Portability**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>


So far we've built an object handling load balancing, routing, and content manipulation across multiple sites.
XC refers to these as "load balancers" but it's really the holistic representation of a service whose components live across a distributed network.
Our object is a simplified representation that does not include WAAP, API Protection, or service policies.
XC is incredibly flexible in defining where that object is advertised.

<div style="height:25px"></div>

### **Exercise 1: Advertise Policy**

-- advertise from the Virtual Site

<div style="height:25px"></div>

#### **Test Criteria**

```http
GET https://eph-ns.mcn-lab.f5demos.com/ HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "env": "azure",
  ...
}
```

<div class="left-aligned-button-container">
    <button id="requestBtn1" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result1" class="mt-3"></div>
<script>
document.getElementById('requestBtn1').addEventListener('click', () => {
    makeHttpRequest('requestBtn1', '/_manip1', 'result');
});
</script>

<div style="height:25px"></div>

### **Exercise 2: Find a Friend (Optional)**

Test a friend's site. Look at the headers from the previous exercises.

We need an input button for the friend's LB. I can keep my funny name LB around for this as well. 

<div style="height:25px"></div>

#### **Test Criteria**

```http
GET https://eph-ns.mcn-lab.f5demos.com/ HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "env": "azure",
  ...
}
```

<div class="left-aligned-button-container">
    <button id="requestBtn2" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result2" class="mt-3"></div>
<script>
document.getElementById('requestBtn2').addEventListener('click', () => {
    makeHttpRequest('requestBtn2', '/_manip2', 'result2');
});
</script>

<div  style="height:25px" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

Nice 🚀! If you've completed all the exercises so far, you have a good foundation for how App Connect addresses common L7 MCN scenarios.
In subsequent labs, we'll explore security and observabilty concepts that build on MCN functionality.
Head over to the <a href="/vnet" class="alert-link">Network Connect</a> exercise.

