package com.example.detecting_humans_in_sar;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.squareup.picasso.Picasso;

public class custom_view_detection extends BaseAdapter {
    String[]date,image;

    private Context context;
    public custom_view_detection(Context applicationContext, String[] date, String[] image) {
        this.context=applicationContext;
        this.date=date;
        this.image=image;
    }


    @Override
    public int getCount() {
        return date.length;
    }

    @Override
    public Object getItem(int i) {
        return null;
    }

    @Override
    public long getItemId(int i) {
        return 0;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        LayoutInflater inflator=(LayoutInflater)context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);

        View gridView;
        if(view==null)
        {
            gridView=new View(context);
            //gridView=inflator.inflate(R.layout.customview, null);
            gridView=inflator.inflate(R.layout.activity_custom_view_detection,null);

        }
        else
        {
            gridView=(View)view;

        }
        TextView tv_date=(TextView)gridView.findViewById(R.id.textView12);
        tv_date.setTextColor(Color.BLACK);
        tv_date.setText(date[i]);

        ImageView im_image=(ImageView) gridView.findViewById(R.id.imageView3);


        SharedPreferences sh= PreferenceManager.getDefaultSharedPreferences(context);
        String ip=sh.getString("ipaddress","");

        String url="http://" + ip + ":5000"+image[i];
        Log.d("urlllllllllllllllllll",url);



        Picasso.with(context).load(url).into(im_image);


        return gridView;
    }
}