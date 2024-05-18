const mysql = require('mysql2');
require('dotenv').config();

//console.log(`process`,process.env) -> pool잘 들어갔는지 확인 가능

const pool = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PW,
    port: process.env.DB_PORT,
    database: process.env.DB_NAME,
    insecureAuth: true,
  });

  

module.exports = pool