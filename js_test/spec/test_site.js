describe("helper functions' expected behavior", function() {

    before(function() {
        this.server = sinon.fakeServer.create();
        this.server.respondWith("GET", "/people/autocomplete/",
           [200, { "Content-Type": "application/json" },
            '["Cornelius Tacitus", "Caecilius Macrinus"]'
            ]);
        this.server.autoRespond = true
    });

    after(function() {
        this.server.restore();
    });

    it("should unobfuscate email addresses on page load", function() {
        $("#test-address").attr('href').should.equal("mailto:address@foo.com")
    });
    /*
    it("should make an ajax query using getAutocomplete()", function() {
        const request = {'q': 'ac'}
        const spy = sinon.spy()
        const result = getAutocomplete(request, spy);
        spy.called.should.equal(true);
    });
    */
});
