var expect = require("expect.js");
var dbReader = require("../lib/dbReader.js")

var sqlite3 = require('sqlite3').verbose();


// Add tests for some main libs
describe("DB Wrapper", function(){
  var database = new sqlite3.Database(":memory:");
  require("../config/db.js")(database);

  var db = new dbReader(database);
  describe("#constructor", function(){
    it("should return an object", function(){
      expect(db).to.be.an("object");
    });
    it("should have all the methods", function(){
      expect(db.findById).to.be.a("function");
      expect(db.getIdFromUsername).to.be.a("function");
      expect(db.numUsers).to.be.a("function");
      expect(db.doesExist).to.be.a("function");
      expect(db.createNewUser).to.be.a("function");
      expect(db.verify).to.be.a("function");
      expect(db.verifyUser).to.be.a("function");
      expect(db.updateLogin).to.be.a("function");
      expect(db.changePassword).to.be.a("function");
      expect(db.reportFailedLogin).to.be.a("function");
      expect(db.getAccessStatus).to.be.a("function");
      expect(db.isAdmin).to.be.a("function");
      expect(db.isIpBlocked).to.be.a("function");
      expect(db.updateAdminPower).to.be.a("function");
      expect(db.checkFormData).to.be.a("function");
      expect(db.addSocket).to.be.a("function");
      expect(db.removeSocket).to.be.a("function");
      expect(db.isSocketBanned).to.be.a("function");
      expect(db.socketUserId).to.be.a("function");
    });
  });
});

describe("PiStat", function(){
  var Stat = require("../lib/pistat.js");
  var pistat = new Stat();
  describe("#constructor", function(){
    it("should return and object", function(){
      expect(pistat).to.be.an("object");
    });
    it("should have all the properties", function(){
      expect(pistat.os).to.be(require("os").type());
      expect(pistat.bootDate).to.be.a(Date);
    });
    it("should have all the functions", function(){
      expect(pistat._load).to.be.a("function");
      expect(pistat._getMemInfo).to.be.a("function");
      expect(pistat._getCpuInfo).to.be.a("function");
      expect(pistat.getSystemInfo).to.be.a("function");
    });
  });
  describe("_load", function(){

  });
  describe("_getMemInfo", function(){
    var res = pistat._getMemInfo();
    it("should return an object", function(){
      expect(res).to.be.an("object");
    });
    it("should return the info about memory", function(){
      expect(res.total).to.be.an("number");
      expect(res.free).to.be.an("number");
    });
  });
  describe("_getCpuInfo", function(){
    var res = pistat._getCpuInfo();
    it("should return an object", function(){
      expect(res).to.be.an("object");
    });
    it("should return the info about cpu", function(){
      expect(res.boot).to.be.a(Date);
      expect(res.avload).to.be.an(Array);
      //expect(res.load).to.be.an(Array); // FIXME: implement _load
      expect(res.cpus).to.be.an("object");
    });
  });
  describe("getSystemInfo", function(){
    var res = pistat.getSystemInfo();
    it("should return an object", function(){
      expect(res).to.be.an("object");
    });
    it("should expose info about the system", function(){
      expect(res.cpu).to.be.an("object");
      expect(res.mem).to.be.an("object");
    });
  });
});

describe("ConfigUtil", function(){
  var util = require("../config/lib/configUtil.js");
  describe("#main", function(){
    it("should provide all function", function(){
      expect(util.merge_options).to.be.a("function");
    })
  });
  describe("#merge_options", function(){
    it("should return default function on undefined", function(){
      var testOpts = {
        opt1: "abc",
        opt2: 123
      }
      expect(util.merge_options(undefined, testOpts)).to.eql(testOpts);
    });
    it("should return default function on null", function(){
      var testOpts = {
        opt1: "abc",
        opt2: 123
      }
      expect(util.merge_options(null, testOpts)).to.eql(testOpts);
    });
    it("should return default function on {}", function(){
      var testOpts = {
        opt1: "abc",
        opt2: 123
      }
      expect(util.merge_options({}, testOpts)).to.eql(testOpts);
    });
    it("should override default options", function(){
      var defaultOpts = {
        opt1: "Hello World",
        opt2: 1234,
        opt3: true,
        opt4: null,
        opt5: 5.678,
        opt6: {
          subop: "test"
        }
      }

      var expectedOpts = [
        {
          opt1: "End of world",
          opt2: 1234,
          opt3: true,
          opt4: null,
          opt5: 5.678,
          opt6: {
            subop: "test"
          }
        },
        {
          opt1: "Hello World",
          opt2: "Test",
          opt3: true,
          opt4: null,
          opt5: 123,
          opt6: {
            subop: "test"
          }
        },
        {
          opt1: "Hello World",
          opt2: 1234,
          opt3: true,
          opt4: null,
          opt5: 5.678,
          opt6: {},
          opt7: null
        },
        {
          opt1: "Hello World",
          opt2: 1234,
          opt3: true,
          opt4: true,
          opt5: 5.678,
          opt6: {
            subop: "test"
          },
          other: "Testing"
        },
        {
          opt1: "Hello World",
          opt2: 1234,
          opt3: true,
          opt4: null,
          opt5: null,
          opt6: {
            subop: "test"
          },
          opt7: "aloha"
        },
        {
          opt1: "Modified",
          opt2: 4321,
          opt3: false,
          opt4: "Hello",
          opt5: -3.1415,
          opt6: {
            subop: "",
            other: "123",
            testing: 123
          },
          opt7: "hi"
        },
        {
          opt1: "Hello World",
          opt2: 1234,
          opt3: true,
          opt4: null,
          opt5: 5.678,
          opt6: {
            subop: "test"
          },
          other: 123,
          more: "Hello",
          someMore: 34343,
          "crazYName345$@#@#": Infinity
        }
      ]

      expect(util.merge_options({}, defaultOpts)).to.eql(defaultOpts);
      expect(util.merge_options({
        opt1: "End of world"
      }, defaultOpts)).to.eql(expectedOpts[0]);
      expect(util.merge_options({
        opt2: "Test",
        opt5: 123
      }, defaultOpts)).to.eql(expectedOpts[1]);
      expect(util.merge_options({
        opt6: {},
        opt7: null
      }, defaultOpts)).to.eql(expectedOpts[2]);
      expect(util.merge_options({
        other: "Testing",
        opt4: true
      }, defaultOpts)).to.eql(expectedOpts[3]);
      expect(util.merge_options({
        opt7: "aloha",
        opt5: null
      }, defaultOpts)).to.eql(expectedOpts[4]);
      expect(util.merge_options(expectedOpts[5], defaultOpts)).to.eql(expectedOpts[5]);
      expect(util.merge_options({
        other: 123,
        more: "Hello",
        someMore: 34343,
        "crazYName345$@#@#": Infinity
      }, defaultOpts)).to.eql(expectedOpts[6]);
    });
  });
});
