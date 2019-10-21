$(document).ready(function(){
    $("#qap-modal").load("modal.html")
    qapNavGetProject()
})

function checkResponse(data){
    if(data.status != 500){alert(data.status + "\n" + JSON.stringify(data.responseJSON.detail))}
    else{alert("致命错误")}
}

function actionResponse(alert, msg){
    $("#qap-action-response").modal("show")
    $("#qap-action-response-alert").attr("class", "alert alert-" + alert)
    $("#qap-action-response-msg").text(msg)
    setTimeout(function(){
        $("#qap-action-response").modal("hide")
    }, 1000)
}

function qapNavDashboard(){
    $("#qap-nav-project").attr('class', "nav-link")
    $("#qap-nav-connection").attr('class', "nav-link")
    $("#qap-nav-dashboard").attr('class', "nav-link active")
    $("#qap-data").load("dashboard.html")
}

function qapNavGetProject(){
    $("#qap-nav-project").attr('class', "nav-link active")
    $("#qap-nav-connection").attr('class', "nav-link")
    $("#qap-nav-dashboard").attr('class', "nav-link")
    $("#qap-data").load("project.html #qap-data-project")
    
    $.get(
        "/api/sprint", 
        function(data, status){
            var text = ""
            for(var i=0;i<data.detail.count;i++){
                text += "<tr>"
                text += "<td>" + data.detail.results[i].project_name + "</td>"
                text += "<td>" + data.detail.results[i].sprint_name + "</td>"
                if(data.detail.results[i].active == "enable"){
                    text += "<td><span class='badge badge-success'>已激活</span></td>"
                }
                else if(data.detail.results[i].active == "disable"){
                    text += "<td><span class='badge badge-secondary'>已暂停</span></td>"
                }
                else if(data.detail.results[i].active == "delete"){
                    text += "<td><span class='badge badge-secondary'>已删除</span></td>"
                }
                else{
                    text += "<td><span class='badge badge-secondary'>未知</span></td>"
                }
                text += "<td>"
                if(data.detail.results[i].active == "enable"){
                    text += '<span class="badge badge-info btn" onclick="qapGetSprint(\'' + data.detail.results[i].sprint_id + '\')">查看</span> '
                    text += '<span class="badge badge-dark btn" onclick="qapSyncSprint(\'' + data.detail.results[i].sprint_id + '\')">同步</span> '
                }
                else{
                    text += '<span class="badge badge-secondary btn" onclick="qapGetSprint(\'' + data.detail.results[i].sprint_id + '\')">查看</span> '
                    text += '<span class="badge badge-secondary btn" onclick="qapSyncSprint(\'' + data.detail.results[i].sprint_id + '\')">同步</span> '
                }
                text += "</td>"
                text += "</tr>"
            }
            $("#qap-data-project-table").html(text)
        }
    )
}

function qapNavGetConnection(){
    $("#qap-nav-project").attr('class', "nav-link")
    $("#qap-nav-connection").attr('class', "nav-link active")
    $("#qap-nav-dashboard").attr('class', "nav-link")
    $("#qap-data").load("connection.html #qap-connection")
    
    $.get(
        "/api/connection", 
        function(data, status){
            $("#qap-connection-id").val(data.detail.results[0].connection_id)
            $("#qap-connection-name").val(data.detail.results[0].connection_name)
            $("#qap-connection-issue-server-type").val(data.detail.results[0].issue_server.type)
            $("#qap-connection-issue-server-host").val(data.detail.results[0].issue_server.host)
            $("#qap-connection-issue-server-account").val(data.detail.results[0].issue_server.account)
            $("#qap-connection-case-server-type").val(data.detail.results[0].case_server.type)
            $("#qap-connection-case-server-host").val(data.detail.results[0].case_server.host)
            $("#qap-connection-case-server-account").val(data.detail.results[0].case_server.account)
        }
    )
}

function qapGetConnection(){
    $.get(
        "/api/connection",
        function(data, status){
            var text = ""
            for(i in data.detail.results){
                text += '<option value="' + data.detail.results[i].connection_id + '">' + data.detail.results[i].connection_name + '</option>'
            }
            $("#qap-create-project-connection").html(text)
        }
    )
}

function qapSubmitConnection(){
    if($("#qap-connection-id").val() == "" || undefined || null) {
        $.ajax({
            type: "POST",
            url: "/api/connection",
            contentType: "application/json",
            data: JSON.stringify({
                connection_name: $("#qap-connection-name").val(),
                issue_server: {
                    type: $("#qap-connection-issue-server-type").val(),
                    host: $("#qap-connection-issue-server-host").val(),
                    account: $("#qap-connection-issue-server-account").val(),
                    password: $("#qap-connection-issue-server-password").val(),
                },
                case_server: {
                    type: $("#qap-connection-case-server-type").val(),
                    host: $("#qap-connection-case-server-host").val(),
                    account: $("#qap-connection-case-server-account").val(),
                    password: $("#qap-connection-case-server-password").val()
                }
            }),
            success: function(data, status){
                actionResponse("success", "创建成功")
            },
            error: function(data, status){
                actionResponse("error", "创建失败")
                checkResponse(data)
            }
        })
    }
    else {
        $.ajax({
            type: "PUT",
            url: "/api/connection/" + $("#qap-connection-id").val(),
            contentType: "application/json",
            data: JSON.stringify({
                connection_name: $("#qap-connection-name").val(),
                issue_server: {
                    type: $("#qap-connection-issue-server-type").val(),
                    host: $("#qap-connection-issue-server-host").val(),
                    account: $("#qap-connection-issue-server-account").val(),
                    password: $("#qap-connection-issue-server-password").val(),
                },
                case_server: {
                    type: $("#qap-connection-case-server-type").val(),
                    host: $("#qap-connection-case-server-host").val(),
                    account: $("#qap-connection-case-server-account").val(),
                    password: $("#qap-connection-case-server-password").val()
                }
            }),
            success: function(data, status){
                actionResponse("success", "更新成功")
            },
            error: function(data, status){
                checkResponse(data)
            }
        })
    }
}

function qapGetProject(){
    $.get(
        "/api/project",
        function(data, status){
            var text = ""
            for(i in data.detail.results){
                text += '<option value="' + data.detail.results[i].project_id + '">' + data.detail.results[i].project_name + '</option>'
            }
            $('#qap-sprint-project').html(text)
        }
    )
}

function qapCreateProject(){
    $.ajax({
        type: "post",
        url: "/api/project",
        contentType: "application/json",
        data: JSON.stringify({
            connection_id: $("#qap-create-project-connection").val(),
            project_name: $("#qap-create-project-name").val()
        }),
        success: function(data, status){
            $("#qap-create-project").modal("hide")
            actionResponse("success", "项目创建成功")
        },
        error: function(data, status){
            actionResponse("error", "项目创建失败")
            checkResponse(data)
        }
    })
}

function listTags(tags){
    var text = ""
    for(i in tags){
        text += "<span class=\"badge badge-secondary\">" + tags[i] + "</span> "
    }
    return text
}

function qapGetSprint(sprint_id){
    $("#qap-data").load("sprint.html #qap-data-sprint")
    $.get(
        "/api/sprint/" + sprint_id,
        function(data, status){
            var text = ""
            text += "<tr><td>项目</td><td id='qap-sprint-project-id' value='" + data.detail.project_id + "'>" + data.detail.project_name + "</td></tr>"
            text += "<tr><td>迭代</td><td id='qap-sprint-id' value='" + data.detail.sprint_id + "'>" + data.detail.sprint_name + "</td></tr>"
            text += "<tr><td>产品版本</td><td><span class=\"badge badge-secondary\">" + data.detail.product_version + "</span> </td></tr>"
            text += "<tr><td>问题类型</td><td>" + listTags(data.detail.issue_types) + "</td></tr>"
            text += "<tr><td>功能</td><td>" + listTags(data.detail.features) + "</td></tr>"
            text += "<tr><td>RC</td><td>" + listTags(data.detail.rcs) + "</td></tr>"
            text += "<tr><td>待修复问题</td><td>" + listTags(data.detail.issue_status.fixing) + "</td></tr>"
            text += "<tr><td>已修复问题</td><td>" + listTags(data.detail.issue_status.fixed) + "</td></tr>"
            text += "<tr><td>待验证问题</td><td>" + listTags(data.detail.issue_status.verified) + "</td></tr>"
            text += "<tr><td>类别</td><td>" + listTags(data.detail.issue_categories) + "</td></tr>"
            $("#qap-data-sprint-table").html(text)
        }
    )
}

function qapCreateSprint(){
    $.ajax({
        type: "post",
        url: "/api/sprint",
        contentType: "application/json",
        data: JSON.stringify({
            project_id: $("#qap-sprint-project").val(),
            sprint_name: $("#qap-sprint-name").val(),
            product_version: $("#qap-sprint-product-version").val(),
            issue_types: $("#qap-sprint-issue-types").val().split(","),
            features: $("#qap-sprint-features").val().split(","),
            rcs: $("#qap-sprint-rcs").val().split(","),
            issue_status: {
                fixing: $("#qap-sprint-issue-status-fixing").val().split(","),
                fixed: $("#qap-sprint-issue-status-fixed").val().split(","),
                verified: $("#qap-sprint-issue-status-verified").val().split(",")
            },
            issue_categories: $("#qap-sprint-categories").val().split(","),
        }),
        success: function(data, status){
            $("#qap-sprint").modal("hide")
            actionResponse("success", "迭代创建成功")
        },
        error: function(data, status){
            actionResponse("error", "迭代创建失败")
            checkResponse(data)
        }
    })
}

function qapUpdateSprint(){
    var sprint_id = $("#qap-sprint-id").attr("value")
    qapGetProject()
    $.get(
        "/api/sprint/" + sprint_id,
        function(data, status){
            $("#qap-sprint").modal("show")
            $("#qap-sprint-title").text("迭代信息")
            $("#qap-sprint-project").val(data.detail.project_id)
            $("#qap-sprint-name").val(data.detail.sprint_name)
            $("#qap-sprint-product-version").val(data.detail.product_version)
            $("#qap-sprint-product-issue-types").val(data.detail.issue_types)
            $("#qap-sprint-features").val(data.detail.features)
            $("#qap-sprint-rcs").val(data.detail.rcs)
            $("#qap-sprint-issue-status-fixing").val(data.detail.issue_status.fixing)
            $("#qap-sprint-issue-status-fixed").val(data.detail.issue_status.fixed)
            $("#qap-sprint-issue-status-verified").val(data.detail.issue_status.verified)
            $("#qap-sprint-categories").val(data.detail.issue_categories)
            $("#qap-sprint-submit").attr("onclick", "qapUpdateSprintSubmit('" + sprint_id + "')")
        }
    )
}

function qapUpdateSprintSubmit(sprint_id){
    $.ajax({
        type: "PUT",
        url: "/api/sprint/" + sprint_id,
        contentType: "application/json",
        data: JSON.stringify({
            project_id: $("#qap-sprint-project").val(),
            sprint_name: $("#qap-sprint-name").val(),
            product_version: $("#qap-sprint-product-version").val(),
            issue_types: $("#qap-sprint-issue-types").val().split(","),
            features: $("#qap-sprint-features").val().split(","),
            rcs: $("#qap-sprint-rcs").val().split(","),
            issue_status: {
                fixing: $("#qap-sprint-issue-status-fixing").val().split(","),
                fixed: $("#qap-sprint-issue-status-fixed").val().split(","),
                verified: $("#qap-sprint-issue-status-verified").val().split(",")
            },
            issue_categories: $("#qap-sprint-categories").val().split(","),
        }),
        success: function(data, status){
            $("#qap-sprint").modal("hide")
            actionResponse("success", "迭代更新成功")
            qapGetSprint(sprint_id)
        },
        error: function(data, status){
            checkResponse(data)
        }
    })
}

function qapSyncSprint(sprint_id){
    actionResponse("success", "开始同步")
    $.get(
        "/api/issue/" + sprint_id + "/sync",
        function(data, status){
            actionResponse("success", "同步完成")
        }
    )
}

function qapSyncAllSprint(){
    actionResponse("success", "开始更新同步所有迭代信息")
    $.get(
        "/api/issue/sync",
        function(data, status){
            actionResponse("success", "所有迭代信息同步完成")
        }
    )
}