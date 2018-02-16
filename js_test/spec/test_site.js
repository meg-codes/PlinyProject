describe("helper functions' expected behavior", function() {

    before(function() {
        this.server = sinon.fakeServer.create();
        this.server.respondWith("GET", "/people/autocomplete/?q=ac",
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
    it("should make an ajax query using getAutocomplete()", function() {
        const request = {'term': 'ac'}
        const spy = sinon.spy()
        const result = getAutocomplete(request, spy);
        console.log(spy.called)
        spy.calledWith('["Cornelius Tacitus", "Caecilius Macrinus"]').should.equal(true);
    });
});
