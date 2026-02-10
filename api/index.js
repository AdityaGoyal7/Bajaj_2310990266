const express = require('express');
const cors = require('cors');

const app = express();
const EMAIL = process.env.OFFICIAL_EMAIL || 'aditya0266.be23@chitkara.edu.in';

app.use(cors());
app.use(express.json());

// Helper functions
function isPrime(num) {
  if (num <= 1) return false;
  if (num <= 3) return true;
  if (num % 2 === 0) return false;
  for (let i = 3; i * i <= num; i += 2) {
    if (num % i === 0) return false;
  }
  return true;
}

function gcd(a, b) {
  while (b) {
    [a, b] = [b, a % b];
  }
  return Math.abs(a);
}

function lcm(a, b) {
  if (a === 0 || b === 0) return 0;
  return Math.abs((a / gcd(a, b)) * b);
}

function lcmArray(arr) {
  return arr.reduce((acc, val) => lcm(acc, val), 1);
}

function hcfArray(arr) {
  return arr.reduce((acc, val) => gcd(acc, val));
}

function fibonacci(n) {
  if (n <= 0) return [];
  const seq = [0];
  if (n === 1) return seq;
  seq.push(1);
  while (seq.length < n) {
    seq.push(seq[seq.length - 1] + seq[seq.length - 2]);
  }
  return seq.slice(0, n);
}

// GET /health
app.get('/health', (req, res) => {
  res.json({ is_success: true, official_email: EMAIL });
});

// POST /bfhl
app.post('/bfhl', (req, res) => {
  const payload = req.body;

  if (!payload || typeof payload !== 'object') {
    return res.status(400).json({
      is_success: false,
      official_email: EMAIL,
      error: 'invalid_json'
    });
  }

  const keys = Object.keys(payload);
  const allowed = ['fibonacci', 'prime', 'lcm', 'hcf'];

  if (keys.length !== 1) {
    return res.status(400).json({
      is_success: false,
      official_email: EMAIL,
      error: 'request_must_contain_exactly_one_key'
    });
  }

  const key = keys[0];

  if (!allowed.includes(key)) {
    return res.status(400).json({
      is_success: false,
      official_email: EMAIL,
      error: 'invalid_key'
    });
  }

  try {
    let data;

    if (key === 'fibonacci') {
      const n = payload.fibonacci;
      if (typeof n !== 'number' || !Number.isInteger(n)) {
        return res.status(400).json({
          is_success: false,
          official_email: EMAIL,
          error: 'fibonacci_must_be_integer'
        });
      }
      if (n < 0 || n > 1000) {
        return res.status(400).json({
          is_success: false,
          official_email: EMAIL,
          error: 'fibonacci_out_of_bounds'
        });
      }
      data = fibonacci(n);
    } else if (key === 'prime') {
      const arr = payload.prime;
      if (!Array.isArray(arr) || !arr.every(x => Number.isInteger(x))) {
        return res.status(400).json({
          is_success: false,
          official_email: EMAIL,
          error: 'prime_must_be_integer_array'
        });
      }
      data = arr.filter(x => isPrime(x));
    } else if (key === 'lcm') {
      const arr = payload.lcm;
      if (!Array.isArray(arr) || arr.length === 0 || !arr.every(x => Number.isInteger(x))) {
        return res.status(400).json({
          is_success: false,
          official_email: EMAIL,
          error: 'lcm_must_be_nonempty_integer_array'
        });
      }
      data = lcmArray(arr);
    } else if (key === 'hcf') {
      const arr = payload.hcf;
      if (!Array.isArray(arr) || arr.length === 0 || !arr.every(x => Number.isInteger(x))) {
        return res.status(400).json({
          is_success: false,
          official_email: EMAIL,
          error: 'hcf_must_be_nonempty_integer_array'
        });
      }
      data = hcfArray(arr);
    }

    res.json({
      is_success: true,
      official_email: EMAIL,
      data
    });
  } catch (err) {
    res.status(500).json({
      is_success: false,
      official_email: EMAIL,
      error: 'internal_server_error'
    });
  }
});

// 404
app.use((req, res) => {
  res.status(404).json({ detail: 'Not Found' });
});

// Error handler
app.use((err, req, res, next) => {
  res.status(500).json({
    is_success: false,
    official_email: EMAIL,
    error: 'internal_server_error'
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;
