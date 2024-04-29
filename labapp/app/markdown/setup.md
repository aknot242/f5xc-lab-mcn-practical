<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/setup.png" width="300px" height="auto" alt="setup">
</div>

# **Setup**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

Log in to the [lab tenant](https://f5-xc-lab-mcn.console.ves.volterra.io/) and open any namespaced tile (Multi-Cloud App Connect, Distributed Apps, etc.). Your ephemeral NS name is a randomly generated concatenation of _adjective_-_animal_. 

<img src="/static/eph-ns.png" width="500px" height="auto" alt="eph-ns"/>

The ephemeral NS name will be used to derive a unique URL for the load balancer used in these exercises.

<form id="setupForm" action="/setup" method="post">
    <div class="mb-3">
        <label for="ENInput" class="form-label"></label>
        <input type="text" class="form-control" id="ENInput" name="eph_ns" placeholder="Enter ephemeral NS">
    </div>
    <button type="submit" name="action" value="save" class="btn btn-primary">Save</button>
    <button type="button" onclick="clearCookie()" class="btn btn-danger">Clear</button>
</form>
<script>
function clearCookie() {
    var form = document.getElementById('setupForm');
    var input = document.getElementById('ENInput');
    input.value = ''; 
    var hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'action';
    hiddenInput.value = 'clear';
    form.appendChild(hiddenInput);
    form.submit();
}
</script>