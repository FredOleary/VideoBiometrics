var express = require('express');
// var batchData = require('../utilities/batchData');

const db = require('../models/index');
const Device = db.sequelize.models.Device;
var router = express.Router();


router.get('/', function(req, res, next) {
  return Device.findAll({
    raw: true
  }).then(function(result){
    res.send(result);
  }).catch( err =>{
    next(err);
  })
});

router.delete('/', function(req, res, next) {
  return Device.destroy({
     where:{id:req.query.deviceId}
  }).then(function(result){
    res.send(200);
  }).catch( err =>{
    next(err);
  })
});
module.exports = router;
