import axios from "@/libs/request";

export function login(params) {
  return axios.request({
    url: "/account/login/",
    data: params,
    method: "post"
  });
}
