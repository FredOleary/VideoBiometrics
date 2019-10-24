'use strict';
module.exports = (sequelize, DataTypes) => {
  const HeartRate = sequelize.define('HeartRate', {
    greenPkPk: {type: DataTypes.DOUBLE, allowNull:true},
    greenFFT: {type: DataTypes.DOUBLE, allowNull:true},
    fps: {type: DataTypes.DOUBLE, allowNull:true},
    FFTConfidence: {type: DataTypes.DOUBLE, allowNull:true},
    groundTruth: {type: DataTypes.DOUBLE, allowNull:true}
    // verticalFFT: {type: DataTypes.DOUBLE, allowNull:true},
    // sumFFTs: {type: DataTypes.DOUBLE, allowNull:true},
    // correlatedPkPk: {type: DataTypes.DOUBLE, allowNull:true},
    // correlatedFFTs: {type: DataTypes.DOUBLE, allowNull:true},
    // DeviceId: {type: DataTypes.INTEGER, allowNull:false}
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