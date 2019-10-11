$(document).ready(function(){
    $("#qap-modal").load("modal.html")
    qapNavGetProject()
})

function checkResponse(data){
    if(data.status != 500){alert(data.status + "\n" + JSON.stringify(data.responseJSON.detail))}
    else{alert("致命错误")}
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
        "/api/jira/sprint", 
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
    $("#qap-data").load("connection.html #qap-create-connection")
    
    $.get(
        "/api/jira/connection", 
        function(data, status){
            $("#qap-create-connection-server").attr("value", data.detail.server)
            $("#qap-create-connection-account").attr("value", data.detail.account)
            $("#qap-create-connection-password").attr("value", data.detail.password)
            $("#qap-create-connection-id").attr("value", data.detail.connection_id)
        }
    )
}

function qapGetProject(){
    $.get(
        "/api/jira/project",
        function(data, status){
            var text = ""
            for(var i=0;i<data.detail.count;i++){
                text += '<option value="' + data.detail.results[i].project_id + '">' + data.detail.results[i].project_name + '</option>'
            }
            $('#qap-create-sprint-project').html(text)
        }
    )
}

function qapGetConnection(){
    $.get(
        "/api/jira/connection",
        function(data, status){
            var text = '<option value="' + data.detail.connection_id + '">' + data.detail.server + '</option>'
            $("#qap-create-project-connection").html(text)
        }
    )
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
        "/api/jira/sprint/" + sprint_id,
        function(data, status){
            var text = ""
            text += "<tr><td>项目</td><td>" + data.detail.project_name + "</td></tr>"
            text += "<tr><td>迭代</td><td>" + data.detail.sprint_name + "</td></tr>"
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

function qapUpdateSprint(sprint_id){
    qapGetProject()
    $.get(
        "/api/jira/sprint/" + sprint_id,
        function(data, status){
            $("#qap-create-sprint").modal("show")
            $("#qap-create-sprint-title").text("迭代信息")
            $("#qap-create-sprint-project").val(data.detail.project_id)
            $("#qap-create-sprint-name").val(data.detail.sprint_name)
            $("#qap-create-sprint-product-version").val(data.detail.product_version)
            $("#qap-create-sprint-product-issue-types").val(data.detail.issue_types)
            $("#qap-create-sprint-features").val(data.detail.features)
            $("#qap-create-sprint-rcs").val(data.detail.rcs)
            $("#qap-create-sprint-issue-status-fixing").val(data.detail.issue_status.fixing)
            $("#qap-create-sprint-issue-status-fixed").val(data.detail.issue_status.fixed)
            $("#qap-create-sprint-issue-status-verified").val(data.detail.issue_status.verified)
            $("#qap-create-sprint-categories").val(data.detail.issue_categories)
        }
    )
}

function qapCreateProject(){
    $.ajax({
        type: "post",
        url: "/api/jira/project",
        contentType: "application/json",
        data: JSON.stringify({
            connection_id: $("#qap-create-project-connection").val(),
            project_name: $("#qap-create-project-name").val()
        }),
        success: function(data, status){
            $("#qap-create-project").modal("hide")
            $("#qap-create-success").modal("show")
            setTimeout(function(){
                $("#qap-create-success").modal("hide")
            }, 1000)
        },
        error: function(data, status){
            checkResponse(data)
        }
    })
}

function qapCreateSprint(){
    $.ajax({
        type: "post",
        url: "/api/jira/sprint",
        contentType: "application/json",
        data: JSON.stringify({
            project_id: $("#qap-create-sprint-project").val(),
            sprint_name: $("#qap-create-sprint-name").val(),
            product_version: $("#qap-create-sprint-product-version").val(),
            issue_types: $("#qap-create-sprint-product-issue-types").val().split(","),
            features: $("#qap-create-sprint-features").val().split(","),
            rcs: $("#qap-create-sprint-rcs").val().split(","),
            issue_status: {
                fixing: $("#qap-create-sprint-issue-status-fixing").val().split(","),
                fixed: $("#qap-create-sprint-issue-status-fixed").val().split(","),
                verified: $("#qap-create-sprint-issue-status-verified").val().split(",")
            },
            issue_categories: $("#qap-create-sprint-categories").val().split(","),
        }),
        success: function(data, status){
            $("#qap-create-project").modal("hide")
            $("#qap-create-success").modal("show")
            setTimeout(function(){
                $("#qap-create-success").modal("hide")
            }, 1000)
        },
        error: function(data, status){
            checkResponse(data)
        }
    })
}

function qapSyncSprint(sprint_id){
    $("#qap-sync-start").modal("show")
    setTimeout(function(){
        $("#qap-sync-start").modal("hide")
    }, 1000)
    $.get(
        "/api/jira/sprint/" + sprint_id + "/sync",
        function(data, status){
            $("#qap-sync-complete").modal("show")
            setTimeout(function(){
                $("#qap-sync-complete").modal("hide")
            }, 1000)
        }
    )
}

function qapSyncAllSprint(){
    $("#qap-sync-start").modal("show")
    setTimeout(function(){
        $("#qap-sync-start").modal("hide")
    }, 1000)
    $.get(
        "/api/jira/sprint/sync",
        function(data, status){
            alert("所有迭代信息同步完成")
        }
    )
}