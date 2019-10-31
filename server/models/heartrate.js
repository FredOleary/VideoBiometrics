'use strict';
module.exports = (sequelize, DataTypes) => {
  const HeartRate = sequelize.define('HeartRate', {
    colorPkPk: {type: DataTypes.DOUBLE, allowNull:true},
    colorFFT: {type: DataTypes.DOUBLE, allowNull:true},
    fps: {type: DataTypes.DOUBLE, allowNull:true},
    FFTConfidence: {type: DataTypes.DOUBLE, allowNull:true},
    groundTruth: {type: DataTypes.DOUBLE, allowNull:true}
  }, {});
  HeartRate.associate = function(models) {
    HeartRate.belongsTo(models.Device, {
      onDelete: "CASCADE",
      foreignKeyConstraint: true,
      foreignKey: {
        name: 'DeviceId', 
        allowNull: false
      }
    });
  };
  return HeartRate;
};