const chai = require('chai');
const chaiHttp = require('chai-http');
const { app, server } = require('../server');

const expect = chai.expect;
chai.use(chaiHttp);

describe('Character Count Service - Integration Tests', () => {
    // Close the server after tests
    after((done) => {
        server.close(done);
    });

    describe('GET /', () => {
        it('should return correct character count', (done) => {
            chai.request(app)
                .get('/')
                .query({ text: 'hello world' })
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    expect(res.body).to.be.an('object');
                    expect(res.body.error).to.be.false;
                    expect(res.body.answer).to.equal(10);
                    expect(res.body.string).to.equal('Contains 10 characters');
                    done();
                });
        });

        it('should handle empty input', (done) => {
            chai.request(app)
                .get('/')
                .query({ text: '' })
                .end((err, res) => {
                    expect(res).to.have.status(400);
                    expect(res.body.error).to.be.true;
                    expect(res.body.message).to.equal('Input cannot be empty');
                    done();
                });
        });

        it('should handle missing input', (done) => {
            chai.request(app)
                .get('/')
                .end((err, res) => {
                    expect(res).to.have.status(400);
                    expect(res.body.error).to.be.true;
                    done();
                });
        });

        it('should handle special characters', (done) => {
            chai.request(app)
                .get('/')
                .query({ text: 'Hello, World! 🌍' })
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    expect(res.body.error).to.be.false;
                    expect(res.body.answer).to.equal(14);
                    done();
                });
        });
    });
});