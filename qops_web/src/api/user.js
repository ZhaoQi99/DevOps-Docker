import axios from "@/libs/request";

export function login(data) {
  return axios.request({
    url: "/account/login/",
    data: data,
    method: "post"
  });
}

export function listPermission(params) {
  return axios.request({
    url: "/account/permissions/",
    method: "get",
    params: params
  });
}

export function deletePermission(data) {
  return axios.request({
    url: "/account/permissions/",
    method: "delete",
    data: data
  });
}
export function updatePermission(data) {
  return axios.request({
    url: "/account/permissions/",
    method: "put",
    data: data
  });
}
export function createPermission(data) {
  return axios.request({
    url: "/account/permissions/",
    method: "POST",
    data: data
  });
}
export function getSelf() {
  return axios.request({
    url: "/account/self/",
    method: "GET"
  });
}
export function listMenu(params) {
  return axios.request({
    url: "/account/menus/",
    method: "get",
    params: params
  });
}

export function deleteMenu(data) {
  return axios.request({
    url: "/account/menus/",
    method: "delete",
    data: data
  });
}
export function updateMenu(data) {
  return axios.request({
    url: "/account/menus/",
    method: "put",
    data: data
  });
}
export function createMenu(data) {
  return axios.request({
    url: "/account/menus/",
    method: "POST",
    data: data
  });
}
