db.createUser(
        {
            user: "gina",
            pwd: "gina19",
            roles: [
                {
                    role: "readWrite",
                    db: "ginadb"
                }
            ]
        }
);