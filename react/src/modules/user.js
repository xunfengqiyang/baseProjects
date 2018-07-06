export const EVENT_USER_LOGIN = "user/EVENT_USER_LOGIN"
export const EVENT_USER_LOGOUT = "user/EVENT_USER_LOGOUT"


const initialState = {
	isLogin: false
}

export default function userStateUpdate(state = initialState, action) {
	switch (action.type) {
		case EVENT_USER_LOGIN:
			return Object.assign({}, state, {
				isLogin: true
			})
		case EVENT_USER_LOGOUT:
			return Object.assign({}, state, {
				isLogin: false
			})
		default:
			return state;
	}
}

export function setUserLogin() {
	return {
		type: EVENT_USER_LOGIN
	}
}

export function setUserLogout() {
	return {
		type: EVENT_USER_LOGOUT
	}
}
