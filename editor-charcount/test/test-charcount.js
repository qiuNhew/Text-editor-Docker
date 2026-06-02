const chai = require('chai');
const expect = chai.expect;
const charcount = require('../charcount');

describe('Character Count Module - Unit Tests', () => {
    describe('counter function', () => {
        it('should correctly count characters in a string', () => {
            expect(charcount.counter('hello world')).to.equal(10);
            expect(charcount.counter('123')).to.equal(3);
        });

        it('should handle special characters', () => {
            expect(charcount.counter('Hello, World! 123')).to.equal(15);
        });

        it('should handle numbers converted to strings', () => {
            expect(charcount.counter(123)).to.equal(3);
        });

        it('should throw error for empty or null input', () => {
            expect(() => charcount.counter()).to.throw(TypeError);
            expect(() => charcount.counter('')).to.throw(TypeError);
            expect(() => charcount.counter(null)).to.throw(TypeError);
            expect(() => charcount.counter('   ')).to.throw(TypeError);
        });
    });

    describe('validate function', () => {
        it('should return valid for proper input', () => {
            const result = charcount.validate('hello');
            expect(result.valid).to.be.true;
            expect(result.message).to.equal('Valid input');
        });

        it('should return invalid for improper input', () => {
            const result = charcount.validate('');
            expect(result.valid).to.be.false;
            expect(result.message).to.equal('Input cannot be empty');
        });
    });
});