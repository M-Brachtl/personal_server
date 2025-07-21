//lets post points.json

crypto = require('crypto')

crypto.createHash = function(algorithm) {
    if (algorithm === 'sha256') {
        return {
            update: function(data) {
                this.data = data;
                return this;
            },
            digest: function(encoding) {
                return crypto.createHash('sha256').update(this.data).digest(encoding);
            }
        };
    }
    throw new Error('Unsupported hash algorithm');
}
async function generateToken(jsonContent) {
    const hash = crypto.createHash('sha256');
    hash.update("");
    return hash.digest('hex');
}