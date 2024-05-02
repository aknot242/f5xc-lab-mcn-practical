<div style="height:25px"></div>
<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/practical.png" width="700px" height="auto" alt="intro">
</div>

# **Welcome**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

This lab is a <strong>practical</strong> training activity.
Each exercise will ask you to <strong>configure</strong>F5 Distributed Cloud ("XC") objects to reinforce core XC Multi-Cloud Networking ("MCN") concepts. 
Once configured, you will <strong>test</strong> the configuration using this web application.

<div style="height:25px"></div>

## **Getting Started**

When your UDF deployment launched, two automated processes started - Customer Edge ("CE") registration and account provisioning in the <strong><a href="https://f5-xc-lab-mcn.console.ves.volterra.io/" target="_blank">lab tenant</a></strong>.

<div style="height:25px"></div>

### **Customer Edge**

The CE in the UDF deployment will registered with the <strong><a href="https://f5-xc-lab-mcn.console.ves.volterra.io/" target="_blank">lab tenant</a></strong>.
CEs on first launch update software and, often, their OS. This can take ~20 min from when the CE is booted.

This lab app includes an indicator of the CE's site name and status in the navigation pane (👀 look to the left).
The **site name** is needed when configuring the load balancer's <strong>advertise policy</strong>.

<div style="height:25px"></div>

### **Account Provisioning**

Check the email used to launch your UDF deployment for a <strong>welcome</strong> or password reset email from the <strong><a href="https://f5-xc-lab-mcn.console.ves.volterra.io/" target="_blank">lab tenant</a></strong>.
Update your password to log into the tenant.

<p float="left">
<a href="https://f5-xc-lab-mcn.console.ves.volterra.io/" target="_blank">
<img src="/static/email.png" height="300px" width="auth"/>
<img src="/static/password.png" height="300px" width="auth"/>
</a>
</p>

<div style="height:25px"></div>

### **While You Wait**

Here's a few things you can do while waiting for the CE to be registered and provisioned:

<ul class="list-group">
  <li class="list-group-item">
    <i class="bi bi-book"></i>&nbsp; &nbsp;
    Read the lab <strong><a href="/overview">overview</a></strong>.
  </li>
  <li class="list-group-item">
    <i class="bi bi-gear"></i>&nbsp; &nbsp;
    Configure lab <strong><a href="/settings">settings</a></strong> after logging into the tenant.
  </li>
  <li class="list-group-item">
    <i class="bi bi-envelope-exclamation"></i>&nbsp; &nbsp;
    Check for the tenant <strong>welcome</strong> email.
  </li>
  <li class="list-group-item">
    <i class="bi bi-cup-hot"></i></i>&nbsp; &nbsp;
    Get a cup of coffee.
  </li>
  </li>
</ul>

<div  style="height:25px" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

<nav aria-label="labapp nav">
  <ul class="pagination justify-content-end">
    <li class="page-item">
      <a class="page-link" href="/overview">Overview <i class="bi bi-arrow-right-circle-fill"></i></a>
    </li>
  </ul>
</nav>



