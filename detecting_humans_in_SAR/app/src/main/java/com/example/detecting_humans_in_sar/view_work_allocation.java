package com.example.detecting_humans_in_sar;

import androidx.appcompat.app.AppCompatActivity;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class view_work_allocation extends AppCompatActivity {
    String[]wid,date,details,work,address,longitude,latitude,status;
    ListView l2;
    String url;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_work_allocation);
        l2=findViewById(R.id.workalloc);
        SharedPreferences sh=PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        String url=sh.getString("url","")+"/view_work_allocation";



        RequestQueue requestQueue = Volley.newRequestQueue(getApplicationContext());
        //String url;
        StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        //  Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();

                        // response
                        try {
                            JSONObject jsonObj = new JSONObject(response);
                            if (jsonObj.getString("status").equalsIgnoreCase("ok")) {

                                JSONArray js= jsonObj.getJSONArray("data");
                                String[] gamecode = new String[js.length()];
                                wid=new String[js.length()];
                                date=new String[js.length()];
                                details=new String[js.length()];
                                work=new String[js.length()];
                                address=new String[js.length()];
                                longitude=new String[js.length()];
                                latitude=new String[js.length()];
                                status=new String[js.length()];
//                                discription=new String[js.length()];
//                                image=new String[js.length()];
//                                status=new String[js.length()];
//
//                                JSONArray js1= jsonObj.getJSONArray("rating");
//                                rating=new String[js1.length()];

                                for(int i=0;i<js.length();i++)
                                {
                                    JSONObject u=js.getJSONObject(i);
                                    wid[i]=u.getString("wid");
                                    date[i]=u.getString("date");
                                    details[i]=u.getString("details");
                                    work[i]=u.getString("work");
                                    address[i]=u.getString("place")+"\n"+u.getString("pin")+"\n"+u.getString("post");
                                    longitude[i]=u.getString("longitude");
                                    latitude[i]=u.getString("latitude");
                                    status[i]=u.getString("status");
//                                    discription[i]=u.getString("description");
//                                    image[i]=u.getString("image");
//                                    status[i]=u.getString("status");


                                }
//                                for(int i=0;i<js1.length();i++)
//                                {
//                                    JSONObject u=js1.getJSONObject(i);
//                                    rating[i]=u.getString("rating");
//
//                                }

                                // ArrayAdapter<String> adpt=new ArrayAdapter<String>(getApplicationContext(),android.R.layout.simple_list_item_1,name);
                                l2.setAdapter(new custom_view_work_allocation(getApplicationContext(),wid,date,details,work,address,longitude,latitude,status));
                                // l1.setAdapter(new Custom(getApplicationContext(),gamecode,name,type,discription,image,status));
                            }


                            // }
                            else {
                                Toast.makeText(getApplicationContext(), "Not found", Toast.LENGTH_LONG).show();
                            }

                        }    catch (Exception e) {
                            Toast.makeText(getApplicationContext(), "Error" + e.getMessage().toString(), Toast.LENGTH_SHORT).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // error
                        Toast.makeText(getApplicationContext(), "eeeee" + error.toString(), Toast.LENGTH_SHORT).show();
                    }
                }
        ) {
            @Override
            protected Map<String, String> getParams() {
                SharedPreferences sh = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
                Map<String, String> params = new HashMap<String, String>();

              params.put("lid",sh.getString("lid",""));

                return params;
            }
        };

        int MY_SOCKET_TIMEOUT_MS=100000;

        postRequest.setRetryPolicy(new DefaultRetryPolicy(
                MY_SOCKET_TIMEOUT_MS,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestQueue.add(postRequest);
    }
}