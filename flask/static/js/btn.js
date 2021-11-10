$(document).ready(function() {
    /* ==================== MySQL ==================== */
    $("#conn_mysql").click(function() {
        username = $('#mysql_username').val();
        password = $('#mysql_password').val();
        ip_port = $('#mysql_server').val().split(':');
        ip = ip_port[0]
        port = ip_port[1]
        args = 'username=' + username;
        args += '&password=' + password;
        args += '&ip=' + ip;
        args += '&port=' + port;
        $.ajax({
            "type": "GET",
            "dataType": "json",
            "contentType": "application/json",
            "url": 'http://192.168.103.55:5000/mysql/listdbs?' + args,
            "timeout": 30000,
            success: function(result) {
                // clear original options
                children = $('#mysql_db_list').children();
                for (i = 1; i < children.length; ++i) {
                    children[i].remove();
                }
                $('#mysql_db_list')[0].selectedIndex = 0;

                db_list = result['db_list'];
                for (key in db_list) {
                    opt_idx = parseInt(key) + 1
                    $('#mysql_db_list').append('<option value="' + opt_idx + '">' + db_list[key] + '</option>');

                }

                $("#conn_mysql_status").text("Connect MySQL succeeded");
            },
            error: function(jqXHR, JQueryXHR, textStatus) {
                $("#conn_mysql_status").text("Connect MySQL failed");
            }
        });
    });
    $("#mysql_db_list").change(function() {
        username = $('#mysql_username').val();
        password = $('#mysql_password').val();
        ip_port = $('#mysql_server').val().split(':');
        ip = ip_port[0]
        port = ip_port[1]
        args = 'username=' + username;
        args += '&password=' + password;
        args += '&ip=' + ip;
        args += '&port=' + port;

        sel_idx = $(this)[0].selectedIndex;
        if (sel_idx != 0) {
            db_name = $(this).children().eq(sel_idx).text();
            args += '&db_name=' + db_name;
            $.ajax({
                "type": "GET",
                "dataType": "json",
                "contentType": "application/json",
                "url": 'http://192.168.103.55:5000/mysql/listtables?' + args,
                "timeout": 30000,
                success: function(result) {
                    // clear original options
                    children = $('#mysql_table_list').children();
                    for (i = 1; i < children.length; ++i) {
                        children[i].remove();
                    }
                    $('#mysql_table_list')[0].selectedIndex = 0;

                    table_list = result['table_list'];
                    for (key in table_list) {
                        opt_idx = parseInt(key) + 1
                        $('#mysql_table_list').append('<option value="' + opt_idx + '">' + table_list[key] + '</option>');

                    }
                },
                error: function(jqXHR, JQueryXHR, textStatus) {
                    $("#conn_mysql_status").text("Connect MySQL failed");
                }
            });
        } else {
            children = $('#mysql_table_list').children();
            for (i = 1; i < children.length; ++i) {
                children[i].remove();
            }
            $('#mysql_table_list')[0].selectedIndex = 0;
        }
    });
    $("#mysql_table_list").change(function() {
        username = $('#mysql_username').val();
        password = $('#mysql_password').val();
        ip_port = $('#mysql_server').val().split(':');
        ip = ip_port[0]
        port = ip_port[1]
        args = 'username=' + username;
        args += '&password=' + password;
        args += '&ip=' + ip;
        args += '&port=' + port;

        db_sel_idx = $("#mysql_db_list")[0].selectedIndex;
        tbl_sel_idx = $(this)[0].selectedIndex;
        if (tbl_sel_idx != 0) {
            db_name = $("#mysql_db_list").children().eq(db_sel_idx).text();
            tbl_name = $(this).children().eq(tbl_sel_idx).text();
            args += '&db_name=' + db_name;
            args += '&table_name=' + tbl_name;
            $.ajax({
                "type": "GET",
                "dataType": "json",
                "contentType": "application/json",
                "url": 'http://192.168.103.55:5000/mysql/listkeys?' + args,
                "timeout": 30000,
                success: function(result) {
                    // clear original options
                    children = $('#mysql_key_list').children();
                    for (i = 0; i < children.length; ++i) {
                        children[i].remove();
                    }

                    key_list = result['key_list'];
                    for (key in key_list) {
                        opt_idx = parseInt(key) + 1
                        $('#mysql_key_list').append('<option value="' + opt_idx + '">' + key_list[key] + '</option>');
                    }
                },
                error: function(jqXHR, JQueryXHR, textStatus) {
                    $("#conn_mysql_status").text("Connect MySQL failed");
                }
            });
        } else {
            children = $('#mysql_key_list').children();
            for (i = 0; i < children.length; ++i) {
                children[i].remove();
            }
        }
    });
    /* ==================== MySQL ==================== */



    /* =================== MongoDB =================== */
    $("#conn_mongodb").click(function() {
        $.ajax({
            "type": "GET",
            "dataType": "json",
            "contentType": "application/json",
            "url": 'http://192.168.103.55:5000/mongo/listdbs',
            "timeout": 30000,
            success: function(result) {
                // clear original options
                children = $('#mongodb_db_list').children();
                for (i = 1; i < children.length; ++i) {
                    children[i].remove();
                }
                $('#mongodb_db_list')[0].selectedIndex = 0;

                db_list = result['db_list'];
                for (key in db_list) {
                    opt_idx = parseInt(key) + 1
                    $('#mongodb_db_list').append('<option value="' + opt_idx + '">' + db_list[key] + '</option>');

                }

                $("#conn_mongodb_status").text("Connect MongoDB succeeded");
            },
            error: function(jqXHR, JQueryXHR, textStatus) {
                $("#conn_mongodb_status").text("Connect MongoDB failed");
            }
        });
    });
    $("#mongodb_db_list").change(function() {
        sel_idx = $(this)[0].selectedIndex;
        if (sel_idx != 0) {
            db_name = $(this).children().eq(sel_idx).text();
            $.ajax({
                "type": "GET",
                "dataType": "json",
                "contentType": "application/json",
                "url": 'http://192.168.103.55:5000/mongo/listcollections?db_name=' + db_name,
                "timeout": 30000,
                success: function(result) {
                    // clear original options
                    children = $('#mongodb_collection_list').children();
                    for (i = 1; i < children.length; ++i) {
                        children[i].remove();
                    }
                    $('#mongodb_collection_list')[0].selectedIndex = 0;

                    collection_list = result['collection_list'];
                    for (key in collection_list) {
                        opt_idx = parseInt(key) + 1
                        $('#mongodb_collection_list').append('<option value="' + opt_idx + '">' + collection_list[key] + '</option>');

                    }
                },
                error: function(jqXHR, JQueryXHR, textStatus) {
                    $("#conn_mongodb_status").text("Connect MongoDB failed");
                }
            });
        } else {
            children = $('#mongodb_collection_list').children();
            for (i = 1; i < children.length; ++i) {
                children[i].remove();
            }
            $('#mongodb_collection_list')[0].selectedIndex = 0;
        }
    });
    $("#mongodb_collection_list").change(function() {
        db_sel_idx = $("#mongodb_db_list")[0].selectedIndex;
        tbl_sel_idx = $(this)[0].selectedIndex;
        if (tbl_sel_idx != 0) {
            db_name = $("#mongodb_db_list").children().eq(db_sel_idx).text();
            tbl_name = $(this).children().eq(tbl_sel_idx).text();
            $.ajax({
                "type": "GET",
                "dataType": "json",
                "contentType": "application/json",
                "url": 'http://192.168.103.55:5000/mongo/listkeys?db_name=' + db_name + '&collection_name=' + tbl_name,
                "timeout": 30000,
                success: function(result) {
                    // clear original options
                    children = $('#mongodb_key_list').children();
                    for (i = 0; i < children.length; ++i) {
                        children[i].remove();
                    }

                    key_list = result['key_list'];
                    key_list.splice(key_list.indexOf('_id'), 1);
                    for (key in key_list) {
                        opt_idx = parseInt(key) + 1
                        $('#mongodb_key_list').append('<option value="' + opt_idx + '">' + key_list[key] + '</option>');
                    }
                },
                error: function(jqXHR, JQueryXHR, textStatus) {
                    $("#conn_mongodb_status").text("Connect MongoDB failed");
                }
            });
        } else {
            children = $('#mongodb_key_list').children();
            for (i = 0; i < children.length; ++i) {
                children[i].remove();
            }
        }
    });
    /* =================== MongoDB =================== */



    /* =================== GenTask =================== */
    function mysql_gen_sql(tbl_name, key_names) {
        sql = 'SELECT ';
        for (i in key_names) {
            key_name = key_names[i]
            sql += key_name + ', ';
        }
        sql = sql.substring(0, sql.length - 2);
        sql += ' FROM ';
        sql += tbl_name;
        sql += ';';
        return sql;
    }

    function mongodb_gen_filter(key_names) {
        field_filter = {
            '_id': 0
        };
        for (i in key_names) {
            key_name = key_names[i];
            field_filter[key_name] = 1
        }
        return field_filter;
    }

    function sql_gen_join(mysql_key_names, mongodb_key_names) {
        const intersections = mysql_key_names.filter(function(n) {
            return mongodb_key_names.indexOf(n) !== -1;
        });
        const diff0 = mysql_key_names.filter(function(n) {
            return mongodb_key_names.indexOf(n) === -1;
        });
        const diff1 = mongodb_key_names.filter(function(n) {
            return mysql_key_names.indexOf(n) === -1;
        });
        if (intersections.length == 0) {
            throw "No intersection between the two groups";
        }

        sql = 'SELECT ';
        for (i in intersections) {
            common_key = intersections[i];
            sql += 'COALESCE(df0.' + common_key + ', df1.' + common_key + ') as ' + common_key + ', ';
        }
        for (i in diff0) {
            key = diff0[i];
            sql += 'df0.' + key + ' as ' + key + ', '
        }
        for (i in diff1) {
            key = diff1[i];
            sql += 'df1.' + key + ' as ' + key + ', '
        }
        sql = sql.substring(0, sql.lastIndexOf(', '));
        sql += ' FROM df0 LEFT JOIN df1 ON ';
        for (i in intersections) {
            common_key = intersections[i];
            sql += 'df0.' + common_key + '=df1.' + common_key + ' AND ';
        }
        sql = sql.substring(0, sql.length-4);
        sql += ';';

        /*
        SELECT 
            COALESCE(df0.ID, df1.ID) as ID, 
            df0.Chinese as Chinese, 
            df0.Math as Math, 
            df1.MartialArts as MartialArts, 
            df1.Swim as Swim 
            FROM df0 
            LEFT JOIN df1 
            ON df0.ID=df1.ID
        */
       return sql;
    }

    function gen_task_info(
            task_id,
            mysql_username, mysql_password, mysql_ip, mysql_port,
            mysql_db_name, mysql_sql,
            mongodb_username, mongodb_password, mongodb_ip, mongodb_port, 
            mongodb_db_name, mongodb_collection_name, mongodb_filter,
            join_sql,
            hds_sql, hds_table, hds_columns
    ){
        task_info = {
            'task_id': task_id,
            'db': [
                {
                    'type': 'mysql',
                    'username': mysql_username,
                    'password': mysql_password,
                    'ip': mysql_ip,
                    'port': mysql_port,
                    'db': mysql_db_name,
                    'sql': mysql_sql
                },
                {
                    'type': 'mongodb',
                    'username': mongodb_username,
                    'password': mongodb_password,
                    'ip': mongodb_ip,
                    'port': mongodb_port,
                    'db': mongodb_db_name,
                    'collection': mongodb_collection_name,
                    'filter': mongodb_filter
                }
            ],
            'join_sql': join_sql,
            'hds': {
                'sql': hds_sql,        // the sql to create table
                'table': hds_table,
                'columns': hds_columns // the column names in table (ordered)
            }
        };

        return task_info;
    }

    function gen_col_opt_elems(mysql_key_names, mongodb_key_names) {
        key_names = mysql_key_names.concat(mongodb_key_names);
        key_names = key_names.filter(function(value, index, self) {
            return self.indexOf(value) === index;
        });

        for (i in key_names) {
            key_name = key_names[i];
            elem = $("#col_opt_template").clone().appendTo($("#col_opt_list")[0]);
            elem.removeAttr('id');
            elem.css('visibility', 'visible');
            elem.children().eq(0).children().eq(0).text(key_name);
            elem.children().eq(1).children().eq(0).attr('id', 'typeopt_'+key_name);
            elem.children().eq(3).children().eq(0).val(key_name);
            elem.children().eq(3).children().eq(1).text(key_name);
            elem.children().eq(3).children().eq(0).prop('checked', true);
        }
    }

    $("#create_req").click(function() {
        mysql_username = $('#mysql_username').val();
        mysql_password = $('#mysql_password').val();
        ip_port = $('#mysql_server').val().split(':');
        mysql_ip = ip_port[0]
        mysql_port = ip_port[1]
        mysql_db_name = $('#mysql_db_list').children()
            .eq($('#mysql_db_list')[0].selectedIndex)
            .text();
        mysql_tbl_name = $('#mysql_table_list').children()
            .eq($('#mysql_table_list')[0].selectedIndex)
            .text();
        mysql_key_sel_idx = $('#mysql_key_list').val();
        mysql_key_names = [];
        for (i in mysql_key_sel_idx) {
            mysql_key_names.push(
                $('#mysql_key_list').children()
                .eq(mysql_key_sel_idx[i] - 1).text());
        }

        mongodb_username = $('#mongodb_username').val();
        mongodb_password = $('#mongodb_password').val();
        ip_port = $('#mongodb_server').val().split(':');
        mongodb_ip = ip_port[0]
        mongodb_port = ip_port[1]
        mongodb_db_name = $('#mongodb_db_list').children()
            .eq($('#mongodb_db_list')[0].selectedIndex)
            .text();
        mongodb_collection_name = $('#mongodb_collection_list').children()
            .eq($('#mongodb_collection_list')[0].selectedIndex)
            .text();
        mongodb_key_sel_idx = $('#mongodb_key_list').val();
        mongodb_key_names = [];
        for (i in mongodb_key_sel_idx) {
            mongodb_key_names.push(
                $('#mongodb_key_list').children()
                .eq(mongodb_key_sel_idx[i] - 1).text());
        }

        mysql_sql = mysql_gen_sql(mysql_tbl_name, mysql_key_names);
        $('#mysql_genres').text(mysql_sql);
        mongodb_filter = mongodb_gen_filter(mongodb_key_names);
        $('#mongodb_genres').text(JSON.stringify(mongodb_filter));

        try {
            join_sql = sql_gen_join(mysql_key_names, mongodb_key_names);
            $('#join_genres').text(join_sql);
        } catch (error) {
            $('#join_genres').text("");
            alert("Error generating JOIN SQL. Message = " + error);
            return;
        }

        gen_col_opt_elems(mysql_key_names, mongodb_key_names);
    });

    function sort_key_info(key_info) {
        primary_key = '';
        for (i in key_info) {
            if (key_info[i]['is_primary']) {
                primary_key = i;
                break;
            }
        }
        key_list = Object.keys(key_info).sort();
        key_list.splice(key_list.indexOf(primary_key), 1);
        key_list.unshift(primary_key);

        const ordered = key_list.reduce(
            (obj, key) => { 
                obj[key] = key_info[key]; 
                return obj;
            }, 
            {}
        );
        return ordered;
    }

    function gen_hds_sql(key_info) {
        key_info = sort_key_info(key_info);
        table_name = $('#hds_table_name').val().replace(/ /g,"_");
        sql = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (';
        for (k in key_info) {
            if (key_info[k]['is_primary']) {
                sql += k + ' ' + key_info[k]['type'] + ' PRIMARY KEY, ';
                break;
            }
        }
        for (k in key_info) {
            if (!key_info[k]['is_primary']) {
                sql += k + ' ' + key_info[k]['type'] + ', ';
            }
        }
        sql = sql.substring(0, sql.length-2);
        sql += ');';
        return sql;
    }

    function gen_hds_columns(key_info) {
        key_info = sort_key_info(key_info);
        col = []
        for (k in key_info) {
            if (key_info[k]['is_primary']) {
                col.push(k);
                break;
            }
        }
        for (k in key_info) {
            if (!key_info[k]['is_primary']) {
                col.push(k);
            }
        }
        return col;
    }
    /* =================== GenTask =================== */



    /* ==================== HDS  ====================== */
    $("#conn_hds").click(function() {
        $.ajax({
            "type": "GET",
            "dataType": "json",
            "contentType": "application/json",
            "url": 'http://192.168.103.151:8000/dataservice/v1/list?from=jdbc:///&info=jdbc:phoenix:192.168.103.151:2181',
            "timeout": 30000,
            success: function(result) {
                // clear original options
                children = $('#hds_table_list').children();
                for (i = 1; i < children.length; ++i) {
                    children[i].remove();
                }
                $('#hds_table_list')[0].selectedIndex = 0;

                table_list = result['dataInfo']['Table name'].split(', ');
                for (key in table_list) {
                    opt_idx = parseInt(key) + 1
                    $('#hds_table_list').append('<option value="' + opt_idx + '">' + table_list[key] + '</option>');
                }
                alert("Connect HDS succeeded");
            },
            error: function(jqXHR, JQueryXHR, textStatus) {
                alert("Connect HDS failed");
            }
        });
    });
    $("#hds_table_list").change(function() {
        tbl_sel_idx = $(this)[0].selectedIndex;
        if (tbl_sel_idx != 0) {
            tbl_name = $(this).children().eq(tbl_sel_idx).text();
            $.ajax({
                "type": "GET",
                "dataType": "json",
                "contentType": "application/json",
                "url": 'http://192.168.103.151:8000/dataservice/v1/list?from=jdbc:///&info=jdbc:phoenix:192.168.103.151:2181' + '&table=' + tbl_name,
                "timeout": 30000,
                success: function(result) {
                    // clear original options
                    children = $('#hds_key_list').children();
                    for (i = 0; i < children.length; ++i) {
                        children[i].remove();
                    }

                    key_list = result['dataInfo']['Column name'].split(', ');
                    for (key in key_list) {
                        opt_idx = parseInt(key) + 1
                        $('#hds_key_list').append('<option value="' + opt_idx + '">' + key_list[key] + '</option>');
                    }
                },
                error: function(jqXHR, JQueryXHR, textStatus) {
                    alert("Connect HDS failed");
                }
            });
        } else {
            children = $('#hds_key_list').children();
            for (i = 0; i < children.length; ++i) {
                children[i].remove();
            }
        }
    });
    /* ==================== HDS  ====================== */

    /* ================== SendTask ==================== */
    // src: https://cythilya.github.io/2017/03/12/uuid/
    function _uuid() {
        var d = Date.now();
        if (typeof performance !== 'undefined' && typeof performance.now === 'function'){
          d += performance.now(); //use high-precision timer if available
        }
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
          var r = (d + Math.random() * 16) % 16 | 0;
          d = Math.floor(d / 16);
            return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
    }
    $("#send_req").click(function() {
        task_id = _uuid();
        $("#sent_task_id").text('task_id = ' + task_id);

        key_info = {}
        primary_key = $('input[name=flexRadioDefault]:checked', '#col_opt_list').val();
        l = $("select[id^=typeopt_]");
        for (i = 0; i < l.length; ++i) {
            key = l.eq(i).attr('id').substring('typeopt_'.length);
            opt = l.eq(i).val();
            key_info[key] = {
                'key': key,
                'type': opt,
                'is_primary': primary_key == key
            }
        }

        hds_sql     = gen_hds_sql(key_info);
        hds_table   = $('#hds_table_name').val().replace(/ /g,"_");
        hds_columns = gen_hds_columns(key_info);

        $("#hds_genres").text(hds_sql);

        task_info = gen_task_info(
            task_id,
            mysql_username, mysql_password, mysql_ip, mysql_port, 
            mysql_db_name, mysql_sql,
            mongodb_username, mongodb_password, mongodb_ip, mongodb_port,
            mongodb_db_name, mongodb_collection_name, mongodb_filter,
            join_sql, hds_sql, hds_table, hds_columns
        );
        $('#task_info').text(JSON.stringify(task_info));


        queue = 'task_req'
        msg   = encodeURI($('#task_info').text());
        $.ajax({
            "type": "POST",
            "xhrFields": {
                "withCredentials": true
            },
            "dataType": "json",
            "contentType": "application/json",
            "url": "http://192.168.103.52:15672/api/exchanges/%2F/amq.default/publish", 
            "data": '{"vhost":"/","name":"amq.default","properties":{"delivery_mode":1,"headers":{}},"routing_key":"'+queue+'","delivery_mode":"1","payload":"'+msg+'","headers":{},"props":{},"payload_encoding":"string"}',
            success: function(result) {
                alert("Message sent");
            },
            error: function(jqXHR, JQueryXHR, textStatus) {
                alert("Error sending message to MQ");
            }
        });
    });
    /* ================== SendTask ==================== */



    /* ================= TaskStatus =================== */
    function send_task_status_req() {
        args = ''
        ids = $('#task_ids').text();
        if (ids !== '') {
            args = '?task_id=' + ids.replace(/\s/g, '');
        }
        $.ajax({
            "type": "GET",
            "dataType": "json",
            "contentType": "application/json",
            "url": 'http://192.168.103.55:5000/taskstatus' + args,
            "timeout": 30000,
            success: function(result) {
                children = $('#task_status_res').children();
                for (i = 1; i < children.length; ++i) {
                    children[i].remove();
                }
                for (i in result) {
                    task = result[i];
                    task_id = task['task_id'];
                    task_scode = task['status'];
                    task_msg = task['message'];
                    task_status = ''
                    switch (task_scode) {
                    case 1:
                        task_status = "ACCEPTED";
                        break;
                    case 2:
                        task_status = "PROCESSING";
                        break;
                    case 3:
                        task_status = "SUCCEEDED";
                        break;
                    case 4:
                        task_status = "FAILED";
                        break;
                    case 5:
                        task_status = "ERROR";
                        break;
                    case 6:
                        task_status = "UNKNOWN";
                        break;
                    }

                    elem = $("#task_res_template").clone().appendTo($("#task_status_res")[0]);
                    elem.removeAttr('id');
                    elem.css('visibility', 'visible');
                    elem.children().eq(0).children().eq(1).text(task_id);
                    elem.children().eq(1).children().eq(1).text(task_status);
                    elem.children().eq(2).children().eq(1).text(task_msg);
                }
            },
            error: function(jqXHR, JQueryXHR, textStatus) {
                alert("Failed to get task status");
            }
        });
    }
    // $("#send_task_status").click(send_task_status_req);
    setInterval(send_task_status_req, 2000);
    /* ================= TaskStatus =================== */
});