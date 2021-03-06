# Django Turbo Response
from turbo_response import TurboFrame


class TestTurboFrame:
    def test_render(self):
        s = TurboFrame("my-form").render("OK")
        assert s == '<turbo-frame id="my-form">OK</turbo-frame>'

    def test_template(self):
        s = TurboFrame("my-form").template("simple.html", {}).render()
        assert "my content" in s
        assert '<turbo-frame id="my-form">' in s

    def test_response(self):
        resp = TurboFrame("my-form").response("OK")
        assert resp.status_code == 200
        assert b"OK" in resp.content
        assert b'<turbo-frame id="my-form"' in resp.content

    def test_template_render(self, rf):
        req = rf.get("/")
        s = TurboFrame("my-form").template("simple.html", {}, request=req).render()
        assert "my content" in s
        assert '<turbo-frame id="my-form"' in s

    def test_template_render_req_in_arg(self, rf):
        req = rf.get("/")
        s = TurboFrame("my-form").template("simple.html", {}).render(request=req)
        assert "my content" in s
        assert '<turbo-frame id="my-form"' in s

    def test_template_response(self, rf):
        req = rf.get("/")
        resp = TurboFrame("my-form").template("simple.html", {}, request=req).response()
        assert resp.status_code == 200
        assert "is_turbo_frame" in resp.context_data
        assert resp._request == req
        content = resp.render().content
        assert b"my content" in content
        assert b'<turbo-frame id="my-form"' in content

    def test_template_response_req_in_arg(self, rf):
        req = rf.get("/")
        resp = TurboFrame("my-form").template("simple.html", {}).response(req)
        assert resp.status_code == 200
        assert "is_turbo_frame" in resp.context_data
        assert resp._request == req
        content = resp.render().content
        assert b"my content" in content
        assert b'<turbo-frame id="my-form"' in content
