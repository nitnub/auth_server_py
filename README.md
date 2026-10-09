# auth_server_py

A rewrite of my [TypeScript authentication project](https://github.com/nitnub/auth-server) in Python w/Flask. This project will use JWTs to authenticate users and allow users to re-authenticate with refresh tokens without having to sign in multiple times. For this version, I plan to add some endpoints for simple email (and possibly text) MFA support. The primary motivator for this rewrite is wanting to write more Python after working with the language at OSU and to work on something light between other commitments after graduating in September. 

## Roadmap
This project is currently in-progress. The below section will be updated as individual components are completed.
- [x] Support docker-compose
- [x] Add ORM (SQLAlchemy w/marshmallow)
- [x] Add JWT support
- [x] Add Redis for token blacklisting
- [x] Swagger for documentation
- [ ] Add email MFA support
- [ ] OAuth 2.0 - Add sign-in with Google
- [ ] OAuth 2.0 - Add sign-in with Microsoft
- [ ] Add text  MFA support (Stretch goal)

