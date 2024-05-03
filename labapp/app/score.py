"""
Build Scoreboards
"""
import copy

score_schema = {
      "/_test1": {
        "name": "Foo Test Example",
        "key": "overview",
        "href": "/overview",
        "result": "none",
    },
    "/_test2": {
        "name": "Bar Test Example",
        "key": "overview",
        "href": "/overview",
        "result": "none"
    },
    "/_lb1": {
        "name": "AWS Cloud App",
        "key": "lb",
        "href": "/loadbalancing",
        "result": "none"
    },
    "/_lb2": {
        "name": "Azure Cloud App",
        "key": "lb",
        "href": "/loadbalancing",
        "result": "none"
    },
    "/_route1": {
        "name": "Path Routing",
        "key": "route",
        "href": "/route",
        "result": "none"
    },
    "/_route2": {
        "name": "Header Routing",
        "key": "route",
        "href": "/route",
        "result": "none"
    },
    "/_manip1:": {
        "name": "Path Rewrite",
        "key": "manip",
        "href": "/manipulation",
        "result": "none"
    },
    "/_manip2": {
        "name": "Request Headers",
        "key": "manip",
        "href": "/manipulation",
        "result": "none"
    },
    "/_manip3": {
        "name": "Response Headers",
        "key": "manip",
        "href": "/manipulation",
        "result": "none"
    },
    "/_port1": {
        "name": "Advertise Policy",
        "key": "port",
        "href": "/portability",
        "result": "none"
    },
    "/_port2": {
        "name": "Find a Friend",
        "key": "port",
        "href": "/portability",
        "result": "none"
    }
}

result_map = {
    "fail": '<i class="bi bi-x-circle-fill score-fail"></i>',
    "pass": '<i class="bi bi-check-circle-fill score-pass"></i>',
    "none": '<i class="bi bi-circle-fill score-unknown"></i>'
}

def score_get_results(cookie_results):
    """
    build score result from cookie
    """
    this_score = copy.deepcopy(score_schema)
    for test_path, result in cookie_results.items():
        if test_path in score_schema:
            this_score[test_path]['result'] = result
    print(this_score)
    print(score_schema)
    return this_score

def score_sort(scores, key):
    """sort score by key"""
    scores = {k: v for k, v in scores.items() if v['key'] == key}
    return scores

def score_build_table(scores, section, name):
    """build table section"""
    section_scores = score_sort(scores, section)
    rows_html = ""
    for key, score in section_scores.items():
        print(score['result'])
        r_icon = result_map[score['result']]
        section_html = f"""
        <tr>
        <td>{score['name']}</td>
        <td>{r_icon}</td>
        </tr>
        """
        rows_html += section_html
    html = f"""
    <table class="score-table"">
        <thead>
          <tr>
            <th>{name}</th>
          </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
      </table>
    """
    return html



