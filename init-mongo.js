db = db.getSiblingDB("mydb");

db.createUser({
  user: "appuser",
  pwd: "apppass123",
  roles: [{ role: "readWrite", db: "mydb" }]
});

db.createCollection("cars");