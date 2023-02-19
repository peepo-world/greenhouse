# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import contextlib

from typing import AsyncIterator

import gino

import greenhouse.web


db = gino.Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)


# TODO: NativeLogin


class TwitchLogin(db.Model):
    __tablename__ = 'twitch_login'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String)


@contextlib.asynccontextmanager
async def lifespan(app) -> AsyncIterator[None]:
    async with db.with_bind(str(greenhouse.web.DB_URL)):
        await db.gino.create_all()

        app.state.db = db
        yield
