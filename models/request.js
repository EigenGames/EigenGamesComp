'use strict';
const { Model } = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class Request extends Model {
    static associate(models) {
      // Each Request belongs to a User.
      Request.belongsTo(models.User, { foreignKey: 'userId', as: 'user' });
    }
  }
  Request.init({
    userId: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    requestText: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    status: {
      type: DataTypes.STRING,
      defaultValue: 'in_development'
    }
  }, {
    sequelize,
    modelName: 'Request',
  });
  return Request;
};
